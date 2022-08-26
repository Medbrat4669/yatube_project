from django.test import TestCase

from ..models import Group, Post, User, Comment

TEST_USERNAME = 'test-user'
TEST_POST_TEXT = 'Тест текст поста'
TEST_GROUP_TITLE = 'Тест группа'
TEST_GROUP_SLUG = 'test-slug'
TEST_GROUP_DESCRIPTION = 'Тест описание группы'
TEST_COMMENT_TEXT = 'Тестовый текст комментария'


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=TEST_USERNAME)
        cls.group = Group.objects.create(
            title=TEST_GROUP_TITLE,
            slug=TEST_GROUP_SLUG,
            description=TEST_GROUP_DESCRIPTION,
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=TEST_POST_TEXT,
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user,
            text=TEST_COMMENT_TEXT,
        )
        cls.field_verboses = {
            cls.post: {
                'text': 'Текст поста',
                'pub_date': 'Дата публикации',
                'author': 'Автор',
                'group': 'Группа',
                'image': 'Изображение'
            },
            cls.comment: {
                'post': 'Пост',
                'author': 'Автор комментария',
                'text': 'Текст комментария',
                'created': 'Дата создания',
            },
        }

    def test_models_verbose_names(self):
        """Verbose name в полях моделей совпадают с ожидаемым."""
        for object, verboses_dict in PostModelTest.field_verboses.items():
            for field, verbose_name in verboses_dict.items():
                with self.subTest(field=field):
                    self.assertEqual(
                        object._meta.get_field(field).verbose_name,
                        verbose_name
                    )
