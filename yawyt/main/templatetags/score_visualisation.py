from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter()
def show_score_visualisation(score,profile_image_url):

    return mark_safe('<div class="scoremeter"><div class="scoremeter-part left_part"></div><div class="scoremeter-part right_part"></div><div style="margin-left:'+str(score)+'px;" class="photo_container"><div class="triangle"></div><div class="user_photo"><img src="'+str(profile_image_url)+'"></div></div></div>')