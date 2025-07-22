from django.contrib import admin
from .models import AnonymousReport, CitizenReport, Profile, ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'message_preview', 'timestamp', 'is_agent_broadcast']
    list_filter = ['timestamp', 'is_agent_broadcast', 'sender__groups']
    search_fields = ['message', 'sender__username']
    readonly_fields = ['timestamp']
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'


# Register your models here.
admin.site.register(AnonymousReport)
admin.site.register(CitizenReport)
admin.site.register(Profile)
