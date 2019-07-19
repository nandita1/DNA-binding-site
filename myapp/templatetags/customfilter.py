from django import template
from django.utils.html import mark_safe
import re
register = template.Library()

@register.filter
def highlight(text,args):
    text = text.replace(args,"<span style='background-color: red'>%s</span>" % args)
    return mark_safe(text)
