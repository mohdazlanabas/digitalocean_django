from django.shortcuts import render
from django.http import HttpResponse

def hello_world(request):
    """Simple view that returns Hello World"""
    return render(request, 'hello/index.html')
