from django.urls import path
from django.views.generic import TemplateView

from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('list-notices', list_notices, name='list_notices'),
    path('upload', upload, name='upload'),
    path('view-keywords', view_keywords, name='view_keywords'),
    path('add-items', add_items, name='add_items'),
    path('download', download, name='download')
]

keyword_urls = [
    path('keywords/', KeywordCrudView.as_view(action='list', permission_required='home.view_noticekeyword'), name='list_keywords'),
    path('keywords/create/', KeywordCrudView.as_view(action='create', permission_required='home.add_noticekeyword'), name='create_keyword'),
    path('keywords/update/<int:pk>/', KeywordCrudView.as_view(action='update', permission_required='home.change_noticekeyword'), name='update_keyword'),
    path('keywords/delete/<int:pk>/', KeywordCrudView.as_view(action='delete', permission_required='home.delete_noticekeyword'), name='delete_keyword'),
]

urlpatterns += keyword_urls
