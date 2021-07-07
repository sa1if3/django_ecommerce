from django.db import models
from crum import get_current_user
# Create your models here.
class QuickNotifications(models.Model):
    message = models.CharField(max_length=500,null=True,blank=True)
    read_status = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        'auth.User', blank=True, null=True, default=None, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "1. Quick Notifications/Alerts"
    
    def __str__(self):
        return self.message