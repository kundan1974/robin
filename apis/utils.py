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
        Profile model require
    """
    # S1: fetch all user whose having expotoken (expotoken, user_id)
    # S2 Call send_push_notofications_to_user in for loop passing above parameters (expotoken, user_id)

def send_push_notofications_to_user(msg,  user_id = "", expo_token = "" ):
    """
    pass
    """
    # S1 Get expotoken for specificed user_id
    # call send_push_notification


