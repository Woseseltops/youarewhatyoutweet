from main.twitterlib import connection

def get_profile_image_url(user,passwordfolder):

    twitterconnection = connection.create_twitter_connection(passwordfolder)
    return twitterconnection.show_user(screen_name=user)['profile_image_url'];
