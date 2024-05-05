from django.contrib import admin
from .models import Item, Notice, NoticeKeyword

# Register your models here.
admin.site.register(Notice)
admin.site.register(NoticeKeyword)
admin.site.register(Item)
