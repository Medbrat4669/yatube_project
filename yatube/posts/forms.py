from django.forms import ModelForm

from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group', 'image']
        labels = {
            'group': 'Группа',
            'text': 'Текст',
        }
        help_texts = {
            'group': 'Вы можете выбрать раздел сообщества, '
            'к которому будет принадлежать эта запись.',
            'text': 'Обязательное поле.',
            'image': 'Выберите изображение для загрузки.',
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text',]
        labels = {'text': 'Текст',}
