from django import template

register = template.Library()

@register.filter
def show_tweet(id):
    return 'Here comes tweet with id '+str(id)