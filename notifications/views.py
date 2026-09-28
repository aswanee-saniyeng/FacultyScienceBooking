from django.http import JsonResponse
import json


def line_webhook(request):
    """
    Receive webhook events from LINE.
    """

    if request.method != 'POST':
        return JsonResponse({
            'message': 'LINE Webhook is working.'
        })

    try:
        data = json.loads(request.body)

        print("LINE WEBHOOK DATA:")
        print(json.dumps(data, indent=2, ensure_ascii=False))

        return JsonResponse({
            'status': 'ok'
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON'
        }, status=400)