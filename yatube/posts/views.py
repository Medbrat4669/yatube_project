from django.shortcuts import get_object_or_404, render
from django.conf import settings

from .models import Post, Group


def index(request):
    posts = Post.objects.all()[:settings.SORT_POSTS]
    template = 'posts/index.html'
    context = {
        'posts': posts,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group)[:settings.SORT_POSTS]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, template, context)
