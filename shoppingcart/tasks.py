from celery import shared_task
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from pingsms import send_single_sms


@shared_task
def send_notification_email_task(context, email_from, recipient_list, subject):
    html_message = render_to_string('email/common.html', context)
    plain_message = strip_tags(html_message)
    if settings.EMAIL_SEND:
        mail.send_mail(subject, plain_message, email_from,
                       recipient_list, html_message=html_message)
    else:
        print('Email Notification is disabled. Check EMAIL_SEND in settings.py!')
        return False


@shared_task
def send_notification_single_sms_task(mobile, message):
    custom_data = {
        "key": settings.PINGSMS_API_KEY,
        "product": "1",
        "language": "1",
        "sender": settings.PINGMS_SENDER_ID,
        "mobile": mobile,
        "template": settings.PINGMS_SINGLE_SMS_TEMPLATE,
        "message": message,
    }
    if settings.SMS_SEND:
        send_single_sms(custom_data)
    else:
        print('SMS Notification is disabled. Check SMS_SEND in settings.py!')
        return False
