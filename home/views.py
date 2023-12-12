from email.policy import default
from django.shortcuts import render
from .models import Notice
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Max

# Create your views here.

notice_length = Notice.objects.all().__len__()

def index(request):
    global notice_length
    loginStatus = True
    current_length = Notice.objects.all().__len__()
    if current_length > notice_length:
        maxID :int = Notice.objects.aggregate(Max('id'))['id__max']
        newNotice = Notice.objects.get(id=maxID)
        to_list1 =  list(User.objects.values_list('email'))
        to_list = []
        for item in to_list1:
            to_list.append(item[0])
        mail = EmailMessage(f'Notice: {newNotice.title}', newNotice.short_description, settings.EMAIL_HOST_USER, to_list)
        print(newNotice.file)
        mail.attach_file(str(newNotice.file))
        mail.send()
        notice_length = current_length
    if request.user.is_anonymous:
        loginStatus = False
    context = {
        'notices': Notice.objects.all(),
        'loginStatus': loginStatus,
        'user': request.user
    }
    return render(request, 'index.html', context)


def upload(request):
    return render(request, 'upload.html')
