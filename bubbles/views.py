from django.shortcuts import render

def index(request):
    return render(request, 'bubbles/index.html', None)
