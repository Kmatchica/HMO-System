from django.shortcuts import redirect

class ErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if exception.__class__.__name__ == 'PermissionDenied':
            return redirect('/login/login')