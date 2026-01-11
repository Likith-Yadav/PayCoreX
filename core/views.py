from django.http import JsonResponse


def health_check(request):
    """Health check endpoint"""
    return JsonResponse({
        'status': 'ok',
        'service': 'PayCoreX',
        'version': '1.0.0'
    })

