from django.http import JsonResponse


def error_404(request, exception):

    data = {"error": {"code": "not_found", "message": "Page not found."}}
    response = JsonResponse(data)
    response.status_code = 404

    return response
