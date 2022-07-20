from django.shortcuts import render
from .models import Post

def index(request):
    posts = Post.objects.order_by('-pub_date')[:10]
    title1 = 'Это главная страница проекта Yatube'
    context = {
        'posts': posts,
        'title1':title1
    }
    return render(request, 'posts/index.html', context) 


def group_posts(request):
    template = 'posts/group_list.html'
    title2 = 'Здесь будет информация о группах проекта Yatube'
    context = {
        'title2':title2
    }
    return render(request, template, context)


