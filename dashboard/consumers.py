
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User, Group
from .models import ChatMessage

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
        data = json.loads(text_data)
        message = data['message']
        message_type = data.get('type', 'chat')
        
        if message_type == 'chat':
            # Save message to database
            chat_message = await self.save_message(self.user, message)
            
            if self.is_agent:
                # Agent sending message to all citizens
                await self.channel_layer.group_send(
                    "citizens",
                    {
                        "type": "chat_message",
                        "message": message,
                        "sender": self.user.username,
                        "timestamp": chat_message.timestamp.strftime('%H:%M'),
                        "is_agent": True
                    }
                )
            else:
                # Citizen sending message to all agents
                await self.channel_layer.group_send(
                    "agents", 
                    {
                        "type": "chat_message",
                        "message": message,
                        "sender": self.user.username,
                        "timestamp": chat_message.timestamp.strftime('%H:%M'),
                        "is_agent": False
                    }
                )
    
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': event['message'],
            'sender': event['sender'], 
            'timestamp': event['timestamp'],
            'is_agent': event['is_agent']
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
    def get_recent_messages(self):
        return list(ChatMessage.objects.select_related('sender').order_by('-timestamp')[:20][::-1])
    
    async def send_recent_messages(self):
        messages = await self.get_recent_messages()
        for msg in messages:
            is_agent = await self.is_law_enforcement_agent(msg.sender)
            await self.send(text_data=json.dumps({
                'type': 'chat',
                'message': msg.message,
                'sender': msg.sender.username,
                'timestamp': msg.timestamp.strftime('%H:%M'),
                'is_agent': is_agent
            }))
