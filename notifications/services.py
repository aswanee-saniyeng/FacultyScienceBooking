import requests
from django.conf import settings


def send_line_message(message):
    """
    Send a text message to LINE Admin.
    """

    url = "https://api.line.me/v2/bot/message/push"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.LINE_CHANNEL_ACCESS_TOKEN}",
    }

    data = {
        "to": settings.LINE_ADMIN_USER_ID,
        "messages": [
            {
                "type": "text",
                "text": message,
            }
        ],
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=10,
    )

    response.raise_for_status()

    return response