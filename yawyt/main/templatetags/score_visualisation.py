from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter()
def show_score_visualisation(score,profile_image_url):

    TOTAL_LINE_LENGTH = 500
    OFFSET_PHOTO_CONTAINER = 14

    length_left_line = score
    length_right_line = TOTAL_LINE_LENGTH - score
    photo_container_left = score + OFFSET_PHOTO_CONTAINER

    return mark_safe('<div class="scoremeter"><div style="width:'+str(length_left_line)+'px;" class="scoremeter-part left_part"></div>' +\
                     '<div class="number_bubble"><div class="number">'+str(score)+'</div></div>' +\
                     '<div style="width:'+str(length_right_line)+'px;" class="scoremeter-part right_part"></div>'+\
                     '<div style="margin-left:'+str(photo_container_left)+'px;" class="photo_container"><div class="triangle"></div><div class="user_photo">' +\
                     '<img src="'+str(profile_image_url)+'"></div></div></div>')