from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings

from .forms import PostForm
from .models import Post, Group, User


def paginator(request, object_list, per_page):
    paginate = Paginator(object_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginate.get_page(page_number)
    return page_obj


def index(request):
    posts = Post.objects.select_related('author', 'group')
    page_obj = paginator(request, posts, settings.SORT_POSTS)
    template = 'posts/index.html'
    context = {
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.groups.select_related('author')
    page_obj = paginator(request, posts, settings.SORT_POSTS)
    template = 'posts/group_list.html'
    context = {
        'group': group,
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    count = author.posts.count()
    page_obj = paginator(request, posts, settings.SORT_POSTS)
    context = {
        'page_obj': page_obj,
        'count': count,
        'author': author,
    }

    template = 'posts/profile.html'

    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post_title = post.text[:30]
    author = post.author
    author_posts = author.posts.all().count()
    context = {
        'post': post,
        'post_title': post_title,
        'author': author,
        'author_posts': author_posts,
    }

    template = 'posts/post_detail.html'

    return render(request, template, context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', request.user)
    form = PostForm()
    groups = Group.objects.all()
    template = 'posts/create_post.html'
    context = {'form': form, 'groups': groups}
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if post.author != request.user:
        return redirect('posts:post_detail', post_id)
    if form.is_valid():
        edited_post = form.save(commit=False)
        edited_post.author = request.user
        edited_post.save()
        return redirect('posts:post_detail', post_id)
    context = {
        'form': form,
        'is_edit': True,
        'post': post,
    }
    template = 'posts/create_post.html'
    return render(request, template, context)
