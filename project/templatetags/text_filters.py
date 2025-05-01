# project/templatetags/text_filters.py
from django import template
import re

register = template.Library()

@register.filter
def clean_bullets(text):
    # Remove *, -, or • bullets
    cleaned = re.sub(r'^\s*[*\-•]\s+', '', text, flags=re.MULTILINE)
    # Remove markdown bold (**text**) and italics (*text*)
    cleaned = re.sub(r'\*\*(.*?)\*\*', r'\1', cleaned)  # bold
    cleaned = re.sub(r'\*(.*?)\*', r'\1', cleaned)      # italic
    return cleaned

