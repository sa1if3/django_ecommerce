from django.contrib import admin
from .models import Profile
# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_filter = ("user","email_confirmed")
    list_display = ("id","user","email_confirmed")
    search_fields = ("user","email_confirmed")