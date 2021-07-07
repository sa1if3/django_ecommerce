from django.urls import path
from userchats import views
urlpatterns = [
    path('show_user_chat/',views.show_user_chat, name = "show_user_chat"),    
]