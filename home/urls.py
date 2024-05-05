from django.urls import path
from .views import *

urlpatterns = [
    path('list-notices', list_notices, name='list_notices'),
    path('upload', upload, name='upload'),
    path('view-keywords', view_keywords, name='view_keywords'),
    path('add-items', add_items, name='add_items'),
    path('download', download, name='download')
]
