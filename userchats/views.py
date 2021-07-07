from django.shortcuts import render

# Create your views here.

def show_user_chat(request):
    context = {}
    return render(request,'userchats/show.html',context)