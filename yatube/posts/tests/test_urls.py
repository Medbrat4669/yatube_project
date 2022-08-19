from django.test import Client, TestCase
from django.urls import reverse
from http import HTTPStatus

from ..models import Group, Post, User

'''
Я сделал как ты  просил, чтобы  автор  побегал по страница
Оставил все тесты как были, но  хз правильно ли,
что ошибки показывать будет по тестам
анонимного пользователя например
(в принципе функционал же ошибка сможет показать )
'''
TEST_USERNAME = 'test-user'
TEST_POST_TEXT = 'Тест текст поста'
TEST_GROUP_TITLE = 'Тест группа'
TEST_GROUP_SLUG = 'test-slug'
TEST_GROUP_DESCRIPTION = 'Тест описание группы'


class PostURLTests(TestCase):
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
            text=TEST_POST_TEXT,
            author=cls.user,
            group=cls.group
        )
        cls.public_pages = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': TEST_GROUP_SLUG}),
            reverse('posts:profile', kwargs={'username': TEST_USERNAME}),
            reverse('posts:post_detail', kwargs={
                'post_id': PostURLTests.post.id})
        ]
        cls.pages_templates = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': TEST_GROUP_SLUG}):
                'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': TEST_USERNAME}):
                'posts/profile.html',
            reverse(
                'posts:post_detail', kwargs={'post_id': PostURLTests.post.id}):
                'posts/post_detail.html',
            reverse(
                'posts:post_edit', kwargs={'post_id': PostURLTests.post.id}):
                'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }

    def setUp(self):
        self.post_author = Client()
        self.post_author.force_login(PostURLTests.user)

    def test_public_pages_exist_at_desired_locations(self):
        """
        Общедоступные страницы пользователя
        (возвращают статус 200).
        """
        for page in PostURLTests.public_pages:
            with self.subTest(page=page):
                response = self.post_author.get(page)
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    f'Страница {page} недоступна!'
                )

    def test_post_create_page_exists_at_desired_location_authorized(self):
        """Страница /create/ доступна авторизованному пользователю."""
        response = self.post_author.get(
            reverse('posts:post_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_create_page_redirect_anonymous_on_login_page(self):
        """
        Страница /create/ перенаправит анонимного пользователя
        на страницу логина.
        """
        response = self.post_author.get(
            reverse('posts:post_create'))
        self.assertRedirects(
            response,
            f"{reverse('users:login')}?next={reverse('posts:post_create')}")

    def test_post_edit_page_exists_at_desired_location_author(self):
        """Страница /<post_id>/edit/ доступна автору поста."""
        response = self.post_author.get(
            reverse(
                'posts:post_edit', kwargs={'post_id': PostURLTests.post.id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit_page_redirect_non_author_on_post_detail_page(self):
        """
        Страница /<post_id>/edit/ перенаправит пользователя, не являющегося
        автором поста, на страницу с информацией о данном посте.
        """
        response = self.post_author.get(
            reverse(
                'posts:post_edit', kwargs={'post_id': PostURLTests.post.id}))
        self.assertRedirects(
            response,
            reverse(
                'posts:post_detail', kwargs={'post_id': PostURLTests.post.id}))

    def test_post_edit_page_redirect_anonymous_on_login_page(self):
        """
        Страница /<post_id>/edit/ перенаправит анонимного пользователя
        на страницу логина.
        """
        post_edit_page = reverse(
            'posts:post_edit', kwargs={'post_id': PostURLTests.post.id})
        response = self.post_author.get(post_edit_page)
        self.assertRedirects(
            response,
            f"{reverse('users:login')}?next={post_edit_page}")

    def test_unexisting_page_is_unavailable(self):
        """Несуществующая страница недоступна (возвращает статус 404)."""
        response = self.post_author.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_urls_uses_correct_template(self):
        """URL-адреса используют соответствующие шаблоны."""
        for reverse_name, template in PostURLTests.pages_templates.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.post_author.get(reverse_name)
                self.assertTemplateUsed(response, template)
