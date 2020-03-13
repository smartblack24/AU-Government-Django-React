from django.contrib import admin
from sitename.admin import admin as sitename_admin

from .models import Mail

class MailAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'gmail_message_id', 'date')
    list_display = ('sender', 'recipient', 'subject', 'date')
    list_display_links = ('subject', )
    fieldsets = (
        (None,
            {'fields': (
                'id', 'gmail_message_id', 'date',
                'sender_name', 'sender_address', 'recipient_name', 'recipient_address',
                'subject', 'snippet', 'content',
                'contacts', 'organisations', 'matter',
                'blocked',
            )},
         ),
    )

    def get_queryset(self, request):
        return self.model.admin_manager.get_queryset()

    def full_name(self, obj):
        return obj.full_name

    def sender(self, obj):
        if obj.sender_name:
            return "{} {}".format(obj.sender_name, obj.sender_address)
        else:
            return obj.sender_address

    def recipient(self, obj):
        if obj.recipient_name:
            return "{} {}".format(obj.recipient_name, obj.recipient_address)
        else:
            return obj.recipient_address

sitename_admin.register(Mail, MailAdmin)
