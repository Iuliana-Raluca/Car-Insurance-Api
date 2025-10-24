from django.http import JsonResponse

def health_ok(request):
    return JsonResponse({"status": "ok"})