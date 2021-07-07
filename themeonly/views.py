from django.shortcuts import render, redirect
from themeonly.forms import CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .tasks import send_registration_email_task
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from themeonly.tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_text
from django.contrib.auth.models import User
# Create your views here.

@login_required(login_url="user_login")
def sample_page(request):
    return render(request, 'themeonly/plain_page.html')


def user_register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            data = request.POST.copy()
            form = CreateUserForm(data)
            if form.is_valid():
                created_user = form.save(commit=False)
                created_user.is_active = False
                created_user.save()
                user = form.cleaned_data.get("username")
                email = form.cleaned_data.get("email")
                app_name = settings.APP_NAME
                app_name_tail = settings.APP_NAME_TAIL
                app_about = settings.APP_ABOUT
                # messages.success(request, 'Account was created for '+user)
                # subject = 'Welcome to '+app_name+"."
                # message = f'Thank you for registering in {app_name}. We hope that you enjoy our App :)'
                # context = {'app_about':app_about,'message': message,'subject':subject,'app_name':app_name, 'user':user}
                # email_from = settings.EMAIL_HOST_USER
                # recipient_list = [email, ]
                # send_registration_email_task.delay(context,email_from,recipient_list,subject)
                current_site = get_current_site(request)
                context = {'user': user,'domain': current_site.domain,'uid': urlsafe_base64_encode(force_bytes(created_user.pk)),
                    'token': account_activation_token.make_token(created_user),'app_name':app_name,'app_name_tail':app_name_tail,'app_about':app_about}                
                subject = 'Activate Your '+app_name+' '+app_name_tail+' Account'
                message = render_to_string('email/account_activation_sent.html', context)
                # created_user.email_user(subject, message)
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email, ]
                send_registration_email_task.delay(context,email_from,recipient_list,subject)
                messages.success(request, 'Account was created for '+str(user)+'. An activation email is sent to verify your Email Id. Please check both your inbox and spam folder!')
                return redirect('user_login')
        context = {'form': form}
        return render(request, 'themeonly/register.html', context)

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        # messages.success(request, 'Congratulations!! Your Email Id has been successfully verified!')
        return redirect('dashboard')
    else:
        return render(request, 'themeonly/account_activation_invalid.html')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Login Failed')
        context = {}
        return render(request, 'themeonly/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('user_login')
