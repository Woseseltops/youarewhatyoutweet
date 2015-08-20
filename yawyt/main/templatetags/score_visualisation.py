from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter()
def show_score_visualisation(score,user):

    return mark_safe('<div class="aggressometer"><div style="margin-left:'+str(score)+'px;" id="photo_container"><div id="triangle"></div><div id="user_photo"><img src="'+str(user)+'"></div></div></div>')