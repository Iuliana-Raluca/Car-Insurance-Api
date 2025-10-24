from rest_framework.views import exception_handler as drf_exception_handler

def api_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    if response is None:
        return response

    data = response.data
    response.data = {"detail": data}
    return response
