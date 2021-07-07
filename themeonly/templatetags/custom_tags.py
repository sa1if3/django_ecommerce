from django import template
from django.conf import settings
register = template.Library()

@register.simple_tag
def app_version():
    return settings.APP_VERSION

@register.simple_tag
def app_name():
    return settings.APP_NAME

@register.simple_tag
def app_name_tail():
    return settings.APP_NAME_TAIL

@register.simple_tag
def app_name_short():
    return settings.APP_NAME_SHORT

@register.simple_tag
def site_url():
    return settings.SITE_URL

@register.simple_tag
def site_email():
    return settings.SITE_EMAIL


@register.simple_tag
def local_timezone():
    return str(settings.LOCAL_TIME_ZONE)