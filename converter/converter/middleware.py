from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseForbidden, Http404


class CustomErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):

        if isinstance(exception, Http404):
            return HttpResponseNotFound(render(request, '404.html'))


        return None