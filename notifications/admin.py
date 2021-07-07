from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(QuickNotifications)
class QuickNotificationsAdmin(admin.ModelAdmin):
    list_display = ("message","read_status","created_by","created_at","updated_at")
