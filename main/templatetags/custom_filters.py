from django import template
from datetime import date
from datetime import datetime
import locale

register = template.Library()

@register.filter
def format_timestamp(value):
    if isinstance(value, datetime):
        locale.setlocale(locale.LC_TIME, 'uz_UZ.UTF-8')  # Adjust this based on your system's locale settings
        return value.strftime('%Y-yil %d-%B')  
    return value





@register.filter  # filterni ro'yxatdan o'tkazish
def feedback_timestamp(value):
    if isinstance(value, datetime):
        locale.setlocale(locale.LC_TIME)  # Locale o'rnatish
        return value.strftime('%Y-%m-%d %H:%M:%S')  # Yil-oy-kun soat:dakika:sekund formatida
    return value



@register.filter()
def course_task(value):
    if isinstance(value, datetime):
        locale.setlocale(locale.LC_TIME)
        return value.strftime('%Y-%m-%d')
    return value




@register.filter
def days_left(value):
    if isinstance(value, (date,)):  # datetime.date turini tekshirish
        today = date.today()
        delta = value - today
        return delta.days if delta.days >= 0 else 0  # Manfiy bo'lmasin
    return 0
