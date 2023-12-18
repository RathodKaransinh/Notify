from django.shortcuts import render
from .models import Notice
from django.contrib.auth.decorators import permission_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

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

@permission_required('home.add_notice')
def upload(request):
    if request.method=='POST':
        title = request.POST['title']
        short_description = request.POST['short_description']
        file = request.FILES['file']
        notice = Notice.objects.create(title = title, short_description = short_description, file = file)
        notice.save()
    
    return render(request, 'upload.html')

