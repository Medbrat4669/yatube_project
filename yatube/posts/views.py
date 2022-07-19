from django.shortcuts import render

def index(request):
    template = 'posts/index.html'
    title1 = 'Это главная страница проекта Yatube'
    context = {
        'title1': title1
    }
    return render(request, template, context) 


def group_list(request):
    template = 'posts/group_list.html'
    title2 = 'Здесь будет информация о группах проекта Yatube'
    context = {
        'title2': title2
    }
    return render(request, template, context)


