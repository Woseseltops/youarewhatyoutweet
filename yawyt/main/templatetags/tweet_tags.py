from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter()
def show_tweet(id):
    return mark_safe('<div class="tweet" id="'+str(id)+'"></div>')
