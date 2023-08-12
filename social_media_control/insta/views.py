from django.shortcuts import render,HttpResponse
from insta.apps import driver

# Create your views here.


def index_page(request):
    return HttpResponse("Site Is Working")