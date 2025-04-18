from django import template
from datetime import datetime
from django.utils import timezone

register = template.Library()

@register.filter
def humanized_date(value):
    if value:
        today = datetime.now().date()
        print(today)
        value = timezone.localtime(value)
        if today == value.date():
            return f"Today at {value.strftime('%I:%M %p')}"
        elif value.date() == today.replace(day=today.day-1):
            return f"Yesterday at {value.strftime('%I:%M %p')}"
        else:
            return value.strftime('%Y-%m-%d %I:%M %p')
    return value.strftime('%Y-%m-%d %I:%M %p')
            