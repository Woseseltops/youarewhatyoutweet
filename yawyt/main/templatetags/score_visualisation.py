from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter()
def show_score_visualisation(score,profile_image_url):

    TOTAL_LINE_LENGTH = 450
    OFFSET_PHOTO_CONTAINER = 22

    percentage_to_pixel_factor = TOTAL_LINE_LENGTH/100
    length_left_line = float(score) * percentage_to_pixel_factor
    length_right_line = TOTAL_LINE_LENGTH - score * percentage_to_pixel_factor
    photo_container_left = score * percentage_to_pixel_factor + OFFSET_PHOTO_CONTAINER

    score_as_str = str(score)
    if len(score_as_str) < 2:
        score_as_str = '0'+score_as_str

    return mark_safe('<div class="scoremeter"><div style="width:'+str(length_left_line)+'px;" class="scoremeter-part left_part"></div>' +\
                     '<div class="number_bubble"><div class="number">'+score_as_str+'<span class="percentage">%</span></div></div>' +\
                     '<div style="width:'+str(length_right_line)+'px;" class="scoremeter-part right_part"></div>'+\
                     '<div style="margin-left:'+str(photo_container_left)+'px;" class="photo_container"><div class="triangle"></div><div class="user_photo">' +\
                     '<img src="'+str(profile_image_url)+'"></div></div></div>')

@register.filter()
def show_fraction_as_percentage(fraction):
    return round(fraction * 100)