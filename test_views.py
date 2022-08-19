from django.test import Client, TestCase
from django.urls import reverse
from django import forms
from django.conf import settings

from ..models import Group, Post, User

TEST_USERNAME = 'test-user'
TEST_POST_TEXT = 'Тест текст поста'
TEST_GROUP_TITLE = 'Тест группа'
TEST_GROUP_SLUG = 'test-slug'
TEST_GROUP_DESCRIPTION = 'Тест описание группы'
TEST_SECOND_GROUP_TITLE = 'Второй тест группа'
TEST_SECOND_GROUP_SLUG = 'test-slug-2'
TEST_SECOND_GROUP_DESCRIPTION = 'Тест описание второй группы'


class PostViewsTests(TestCase):
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
            group=cls.group,
        )
        cls.pages_templates = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': TEST_GROUP_SLUG}):
                'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': TEST_USERNAME}):
                'posts/profile.html',
            reverse(
                'posts:post_detail',
                kwargs={'post_id': PostViewsTests.post.id}):
                'posts/post_detail.html',
            reverse(
                'posts:post_edit', kwargs={'post_id': PostViewsTests.post.id}):
                'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }

    @classmethod
    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostViewsTests.user)

    def post_check(self):
        response = self.authorized_client
        first_post = response.context['page_obj'][0]
        self.assertEqual(first_post.text, TEST_POST_TEXT)

    def test_pages_use_correct_templates(self):
        """URL-адреса используют соответствующие шаблоны."""
        for reverse_name, template in PostViewsTests.pages_templates.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_list_is_1(self):
        """На страницу index передается ожидаемое количество постов."""
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(response.context['page_obj'].paginator.count, 1)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        first_post = response.context['page_obj'][0]
        self.assertEqual(first_post.author, PostViewsTests.user)
        self.assertEqual(first_post.group, PostViewsTests.group)

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': TEST_GROUP_SLUG}))
        first_post = response.context['page_obj'][0]
        self.assertEqual(response.context['group'].title, TEST_GROUP_TITLE)
        self.assertEqual(response.context['group'].slug, TEST_GROUP_SLUG)
        self.assertEqual(
            response.context['group'].description, TEST_GROUP_DESCRIPTION)
        self.assertEqual(first_post.author, PostViewsTests.user)
        self.assertEqual(first_post.group, PostViewsTests.group)

    def test_post_is_not_in_the_wrong_group(self):
        """
        Пост, принадлежащий к Тестовой группе, не попадёт на страницу второй
        тестовой группы (количество постов во второй тестовой группе = 0).
        """
        self.second_group = Group.objects.create(
            title=TEST_SECOND_GROUP_TITLE,
            slug=TEST_SECOND_GROUP_SLUG,
            description=TEST_GROUP_DESCRIPTION,
        )
        response = self.authorized_client.get(reverse(
            'posts:group_list', kwargs={'slug': TEST_SECOND_GROUP_SLUG}))
        self.assertEqual(
            response.context['group'].slug, self.second_group.slug)
        self.assertEqual(response.context['page_obj'].paginator.count, 0)

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': TEST_USERNAME}))
        first_post = response.context['page_obj'][0]
        self.assertEqual(response.context['author'].username, TEST_USERNAME)
        self.assertEqual(first_post.author, PostViewsTests.user)
        self.assertEqual(first_post.group, PostViewsTests.group)

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:post_detail', kwargs={'post_id': PostViewsTests.post.id}))
        self.assertEqual(response.context['post'].text, TEST_POST_TEXT)
        self.assertEqual(response.context['post'].author, PostViewsTests.user)
        self.assertEqual(response.context['post'].group, PostViewsTests.group)

    def test_post_create_page_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_post_edit_page_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:post_edit', kwargs={'post_id': PostViewsTests.post.id}))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)
        self.assertEqual(response.context['is_edit'], True)
        self.assertEqual(response.context['post'].text, TEST_POST_TEXT)
        self.assertEqual(response.context['post'].author, PostViewsTests.user)
        self.assertEqual(response.context['post'].group, PostViewsTests.group)


class PostViewsCacheTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=TEST_USERNAME)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostViewsCacheTest.user)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=TEST_USERNAME)
        cls.group = Group.objects.create(
            title=TEST_GROUP_TITLE,
            slug=TEST_GROUP_SLUG,
            description=TEST_GROUP_DESCRIPTION,
        )
        cls.total_posts_count = 13
        cls.first_page_posts_count = settings.SORT_POSTS
        cls.second_page_posts_count = 3
        Post.objects.bulk_create(Post(
            text=f'Тест пост {post}', author=cls.user, group=cls.group
        ) for post in range(cls.total_posts_count))
        cls.paginator_pages = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': TEST_GROUP_SLUG}),
            reverse('posts:profile', kwargs={'username': TEST_USERNAME})
        ]

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PaginatorViewsTest.user)

    def test_first_page_contains_ten_records(self):
        """На первой странице десять постов."""
        for page in PaginatorViewsTest.paginator_pages:
            with self.subTest(page=page):
                response = self.authorized_client.get(page)
                self.assertEqual(
                    len(response.context['page_obj']),
                    PaginatorViewsTest.first_page_posts_count)

    def test_second_page_contains_three_records(self):
        """На второй странице три поста."""
        for page in PaginatorViewsTest.paginator_pages:
            with self.subTest(page=page):
                response = self.authorized_client.get(page + '?page=2')
                self.assertEqual(
                    len(response.context['page_obj']),
                    PaginatorViewsTest.second_page_posts_count)
