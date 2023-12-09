from django.urls import path
from .views import *


urlpatterns = [
    path('register/', register, name='register'),
    path('', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('home/', home, name='home'),
    path('upload/', upload_file, name='upload_file'),
    path('files/', file_list, name='file_list'),
    path('user/search/', user_search, name='user_search'),
    path('share_files_page/<int:user_id>/', share_files_page, name='share_files_page'),
    path('share_files/', share_files, name='share_files'),
    path('shared_files/', shared_files_view, name='shared_files'),
    path('shared_files/view/<int:shared_file_id>/', view_shared_file, name='view_shared_file'),
    path('shared_files/download/<int:shared_file_id>/', download_shared_file, name='download_shared_file'),

    ]

