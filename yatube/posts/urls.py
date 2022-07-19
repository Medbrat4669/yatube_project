from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('posts/', views.group_list, name='group_list'),
    path('index.html', views.index, name='index'),
    path('', views.index, name='index')
]