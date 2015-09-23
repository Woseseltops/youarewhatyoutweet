$(document).ready(function()
{
	$(".background_image").hide();
	$("#bg0").show();
	current_section = 0;
	reset_backgrounds_except_for_section(0);

	current_background_maximum_scroll_speed = 100
	current_background_scroll_speed = 70;

	$(window).scroll(function()
	{
		pixels_scrolled_down = $(window).scrollTop();

		c = 0;
		height_of_all_sections_investigated_so_far = 0;

		console.log('Start investigation')

		$('.section').each(function()
		{
		    pixels_scrolled_down_in_this_section = pixels_scrolled_down - height_of_all_sections_investigated_so_far;
			height_of_section_investigating = parseInt($(this).css('height'));
			height_of_all_sections_investigated_so_far += height_of_section_investigating;

			if (height_of_all_sections_investigated_so_far > pixels_scrolled_down)
			{
				if (c != current_section)
				{
					console.log('Set the current section to'+c)
					current_section = c;
					reset_backgrounds_except_for_section(0);
					$('#s'+c).css('background-image','url("")');

					$('.background_image').hide();
					$('#bg'+c).show();
				}

				//Set a nice scrolling effect to the current background as well
        		$('#bg'+current_section).css('top',-pixels_scrolled_down_in_this_section/(current_background_maximum_scroll_speed - current_background_scroll_speed));

				return false; //Break the loop
			}
			else
			{
				c++;
			}
		});

	});

	function reset_backgrounds_except_for_section(section_id)
	{
		c2 = 0; //Called c2 because it otherwise messes op the counter in the scroll function
		$('.section').each(function()
		{
			if (c2 != section_id)
			{
			    //Find the background image you need
			    background_of_this_section = $('#bg'+c2).attr('src');
				$('#s'+c2).css('background-image','url("'+background_of_this_section+'")');
			}
			c2++;
		});
	}
});
