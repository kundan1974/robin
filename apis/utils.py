import json
import requests
import asyncio
from users.models import Profile
# user_profile model import 


# NOTE: We can call below funcation everywhere 

def send_push_notification(expo_push_token, msg):
    message = {
        'to': expo_push_token,
        'sound': 'default',
        'title': 'Oncflow doctors',
        'body': str(msg),
        'data': { 'someData': 'goes here' },
    }

    requests.post('https://exp.host/--/api/v2/push/send', headers={
        'Accept': 'application/json',
        'Accept-encoding': 'gzip, deflate',
        'Content-Type': 'application/json',
    }, data=json.dumps(message))



def send_push_notifications_to_all(msg):
    """
    Send push notification to all users
    """
    
    users_with_expo = Profile.objects.filter(expotoken__isnull=False).values_list('expotoken', flat=True)
    
    for expo_token in users_with_expo:
        send_push_notification(expo_token, msg)


def send_push_notofications_to_user(msg,  user_id = "", expo_token = "" ):
    """
    
    """
    if user_id and msg:
        user_with_expo = Profile.objects.filter(user_id=user_id).values_list('expotoken', flat=True)
        send_push_notification(user_with_expo[0], msg)
    


