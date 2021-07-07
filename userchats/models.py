from django.db import models
from crum import get_current_user
# Create your models here.
class UserChats(models.Model):
    # message = models.CharField(max_length=500,null=True,blank=True)
    read_status = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        'auth.User', blank=True, null=True, default=None, on_delete=models.SET_NULL, related_name='sender')
    created_for = models.ForeignKey(
        'auth.User', blank=True, null=True, default=None, on_delete=models.SET_NULL, related_name='receiver')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "1. User Chat Rooms"
    
    def __str__(self):
        return str(self.id)

class UserChatsMessage(models.Model):
    message = models.CharField(max_length=500,null=True,blank=True)
    user_chats = models.ForeignKey('UserChats',null=True,on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'auth.User', blank=True, null=True, default=None, on_delete=models.SET_NULL)
    class Meta:
        verbose_name_plural = "2. User Chats Messages"
    
    def __str__(self):
        return self.message