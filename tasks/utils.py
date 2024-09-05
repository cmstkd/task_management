import requests
from django.conf import settings

def send_sms_via_msg91(to_phone_number, message):
    url = 'https://api.msg91.com/api/v5/flow/'
    payload = {
        'sender': 'SENDER_ID',
        'route': '4',
        'mobiles': to_phone_number,
        'message': message,
        'authkey': settings.MSG91_AUTH_KEY
    }
    response = requests.post(url, data=payload)
    return response.json()

