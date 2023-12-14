from django.shortcuts import render

from .models import Notice

# Create your views here.

def index(request):
    loginStatus = True
    if request.user.is_anonymous:
        loginStatus = False
        
    context = {
        'notices': Notice.objects.all(),
        'loginStatus': loginStatus,
        'user': request.user
    }
    return render(request, 'index.html', context)

