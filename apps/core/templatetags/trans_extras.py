from django import template
from django.utils.translation import gettext, activate, get_language
from django.urls import translate_url

register = template.Library()

@register.filter
def trans_str(value):
    """
    Translates a variable string using gettext.
    Usage: {{ some_variable|trans_str }}
    """
    if not value:
        return ""
    return gettext(str(value))

@register.simple_tag(takes_context=True)
def change_lang(context, lang=None, *args, **kwargs):
    """
    Get active page's url by a specified language
    Usage: {% change_lang 'en' %}
    """
    path = context['request'].path
    return translate_url(path, lang)
