from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group']
        labels = {
            'group': 'Группа',
            'text': 'Текст',
        }
        help_texts = {
            'group': 'Вы можете выбрать раздел сообщества, '
            'к которому будет принадлежать эта запись.',
            'text': 'Обязательное поле.',
        }
