from celery import shared_task
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

@shared_task
def send_registration_email_task(context, email_from, recipient_list, subject):
    html_message = render_to_string('email/account_activation_sent.html', context)
    plain_message = strip_tags(html_message)
    if settings.EMAIL_SEND:
        mail.send_mail(subject, plain_message, email_from,
                   recipient_list, html_message=html_message)
    else:
        print('Email Notification is disabled. Check EMAIL_SEND in settings.py!')
        return False
    
