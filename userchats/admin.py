from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(UserChats)
class UserChatsAdmin(admin.ModelAdmin):
    list_filter = ("read_status","created_at","updated_at")
    list_display = ("id","read_status","created_by","created_for","created_at","updated_at")
    search_fields = ("id","read_status","created_by","created_for","created_at","updated_at")
    readonly_fields = ("id","created_at","updated_at")

    show_full_result_count = False

@admin.register(UserChatsMessage)
class UserChatsMessageAdmin(admin.ModelAdmin):
    list_filter = ("created_at","updated_at")
    list_display = ("id","user_chats","created_by","created_at","updated_at")
    search_fields = ("id","user_chats","created_at","created_at","updated_at")
    readonly_fields = ("id","created_at","updated_at")

    show_full_result_count = False