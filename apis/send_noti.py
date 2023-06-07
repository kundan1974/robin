import json
import requests
import asyncio


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

expo = "ExponentPushToken[GX7VFuDETFA5KbnE1cXGNF]"
msg = "Simulation updated successfully"


send_push_notification(expo,msg)
