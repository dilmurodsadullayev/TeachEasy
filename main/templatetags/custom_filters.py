from django import template
from datetime import datetime
import locale

register = template.Library()

@register.filter
def format_timestamp(value):
    if isinstance(value, datetime):
        locale.setlocale(locale.LC_TIME, 'uz_UZ.UTF-8')  # Adjust this based on your system's locale settings
        return value.strftime('%Y-yil %d-%B')  
    return value
