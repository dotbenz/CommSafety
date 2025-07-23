import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User, Group
from .models import ChatMessage
import asyncio

class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.is_agent = False
        
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return
            
        # Check if user is an agent
        self.is_agent = await self.is_law_enforcement_agent(self.user)
        
        # Add user to appropriate group
        await self.channel_layer.group_add("chat_room", self.channel_name)
        
        if self.is_agent:
            # Agents join the agents group
            await self.channel_layer.group_add("agents", self.channel_name)
            # Notify all citizens that an agent is online
            await self.channel_layer.group_send(
                "citizens",
                {
                    "type": "agent_status",
                    "status": "online",
                    "agent_name": self.user.username
                }
            )
        else:
            # Citizens join the citizens group
            await self.channel_layer.group_add("citizens", self.channel_name)
            
        await self.accept()
        
        # Send recent messages to the user
        await self.send_recent_messages()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("chat_room", self.channel_name)
        
        if self.is_agent:
            await self.channel_layer.group_discard("agents", self.channel_name)
            # Notify citizens that agent went offline
            await self.channel_layer.group_send(
                "citizens",
                {
                    "type": "agent_status",
                    "status": "offline", 
                    "agent_name": self.user.username
                }
            )
        else:
            await self.channel_layer.group_discard("citizens", self.channel_name)
    
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data['message'].strip()
            message_type = data.get('type', 'chat')
            
            if message_type == 'chat' and message:
                # Save message to database
                chat_message = await self.save_message(self.user, message)
                
                # Send message to sender first (for immediate feedback)
                await self.send(text_data=json.dumps({
                    'type': 'chat',
                    'message': message,
                    'sender': self.user.username,
                    'timestamp': chat_message.timestamp.strftime('%H:%M'),
                    'is_agent': self.is_agent,
                    'is_own_message': True
                }))
                
                if not self.is_agent:  # If citizen sends message
                    # Send automatic agent response after a short delay
                    await asyncio.sleep(1)  # 1 second delay for realism
                    
                    # Create and save agent response
                    agent_response = "Hi. This is agent Tony. What is your emergency?"
                    agent_message = await self.save_agent_response(agent_response)
                    
                    # Send agent response to the citizen
                    await self.send(text_data=json.dumps({
                        'type': 'chat',
                        'message': agent_response,
                        'sender': 'Agent Tony',
                        'timestamp': agent_message.timestamp.strftime('%H:%M'),
                        'is_agent': True,
                        'is_own_message': False
                    }))
                
                # Also broadcast to other users in the room
                await self.channel_layer.group_send(
                    "chat_room",
                    {
                        "type": "chat_message",
                        "message": message,
                        "sender": self.user.username,
                        "sender_id": self.user.id,
                        "timestamp": chat_message.timestamp.strftime('%H:%M'),
                        "is_agent": self.is_agent
                    }
                )
                
        except json.JSONDecodeError:
            # Handle invalid JSON
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid message format'
            }))
        except Exception as e:
            # Handle other errors
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Failed to send message'
            }))
    
    async def chat_message(self, event):
        # Don't send message back to sender (they already have it)
        if event['sender_id'] != self.user.id:
            await self.send(text_data=json.dumps({
                'type': 'chat',
                'message': event['message'],
                'sender': event['sender'], 
                'timestamp': event['timestamp'],
                'is_agent': event['is_agent'],
                'is_own_message': False
            }))
    
    async def agent_status(self, event):
        # Send agent status update to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'agent_status',
            'status': event['status'],
            'agent_name': event['agent_name']
        }))
    
    @database_sync_to_async
    def is_law_enforcement_agent(self, user):
        return user.groups.filter(name='Law Enforcement Agents').exists()
    
    @database_sync_to_async
    def save_message(self, sender, message):
        return ChatMessage.objects.create(
            sender=sender,
            message=message,
            is_agent_broadcast=self.is_agent
        )
    
    @database_sync_to_async
    def save_agent_response(self, message):
        # Create a system user for agent responses if it doesn't exist
        agent_user, created = User.objects.get_or_create(
            username='agent_tony',
            defaults={
                'first_name': 'Agent',
                'last_name': 'Tony',
                'is_active': True
            }
        )
        if created:
            # Add to agents group
            agent_group, _ = Group.objects.get_or_create(name='Law Enforcement Agents')
            agent_user.groups.add(agent_group)
        
        return ChatMessage.objects.create(
            sender=agent_user,
            message=message,
            is_agent_broadcast=True
        )
    
    @database_sync_to_async
    def get_recent_messages(self):
        return list(ChatMessage.objects.select_related('sender').order_by('-timestamp')[:20][::-1])
    
    async def send_recent_messages(self):
        messages = await self.get_recent_messages()
        for msg in messages:
            is_agent = await self.is_law_enforcement_agent(msg.sender)
            is_own_message = msg.sender.id == self.user.id
            
            await self.send(text_data=json.dumps({
                'type': 'chat',
                'message': msg.message,
                'sender': msg.sender.username,
                'timestamp': msg.timestamp.strftime('%H:%M'),
                'is_agent': is_agent,
                'is_own_message': is_own_message
            }))