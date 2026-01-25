from django.http import HttpResponse
from django.urls import path


def index(request):
    return HttpResponse('Hello, world!')


urlpatterns = [
    path('', index, name='index'),
]