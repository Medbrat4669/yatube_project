from django.test import Client, TestCase
from django.urls import reverse

from ..forms import PostForm
from ..models import Post, User

'''Думал запихнуть их в settings как мы делали с 'магическими цифрами', 
но думаю, что тесты могут меняться время от времени '''
TEST_USERNAME = 'test-user'
TEST_POST_TEXT = 'Тест текст поста'
TEST_POST_NEW_TEXT = 'Новый текст поста'


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=TEST_USERNAME)
        cls.form = PostForm()

    @classmethod
    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostFormTests.user)

    def test_create_post(self):
        """
        Валидная форма создаёт новую запись Post в базе данных,
        затем перенаправляет на страницу профиля.
        """
        post_count = Post.objects.count()
        form_data = {
            'text': TEST_POST_TEXT,
            'author': PostFormTests.user,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data
        )
        self.assertRedirects(
            response,
            reverse('posts:profile', kwargs={'username': TEST_USERNAME})
        )
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text=TEST_POST_TEXT,
                author=PostFormTests.user
            )
        )

    def test_edit_post(self):
        """Валидная форма изменяет пост с post_id в БД."""
        self.existing_post = Post.objects.create(
            text=TEST_POST_TEXT, author=PostFormTests.user)
        post_count = Post.objects.count()
        form_data = {
            'text': TEST_POST_NEW_TEXT,
            'author': PostFormTests.user
        }
        response = self.authorized_client.post(
            reverse(
                'posts:post_edit', kwargs={'post_id': self.existing_post.id}),
            data=form_data
        )
        self.assertRedirects(
            response,
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.existing_post.id}))
        self.assertEqual(Post.objects.count(), post_count)
        self.assertTrue(
            Post.objects.filter(
                text=TEST_POST_NEW_TEXT,
                author=PostFormTests.user,
            )
        )
