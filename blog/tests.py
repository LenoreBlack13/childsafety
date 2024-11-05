# blog/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment, Category


class BlogTests(TestCase):
    def setUp(self):
        # Создание пользователя
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user.profile.can_create_posts = True
        self.user.profile.save()

        self.category = Category.objects.create(name='Test Category')

        self.post = Post.objects.create(title='Test Title', content='Test Content', author=self.user)
        self.post.categories.add(self.category)

        self.comment = Comment.objects.create(post=self.post, user=self.user, comment='Test Comment')

    def test_post_string_representation(self):
        self.assertEqual(str(self.post), 'Test Title')

    def test_post_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), reverse('post-detail', kwargs={'pk': self.post.pk}))

    def test_post_list_view(self):
        response = self.client.get(reverse('blog-myblog'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Title')

    def test_post_create_view_with_valid_data(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('post-create'), {
            'title': 'New Title',
            'content': 'New Content',
            'categories': [self.category.id],
        })
        # Проверка, что редирект происходит после успешного создания
        self.assertEqual(response.status_code, 302)
        # Проверка, что новый пост был создан
        self.assertTrue(Post.objects.filter(title='New Title').exists())

    def test_post_update_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('post-update', kwargs={'pk': self.post.pk}), {
            'title': 'Updated Title',
            'content': 'Updated Content',
            'categories': [self.category.id],
        })
        self.post.refresh_from_db()
        # Проверка, что редирект происходит после успешного обновления
        self.assertEqual(response.status_code, 302)
        # Проверка, что заголовок был обновлен
        self.assertEqual(self.post.title, 'Updated Title')

    def test_post_delete_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('post-delete', kwargs={'pk': self.post.pk}))
        # Проверка, что удаление поста произошло и происходит редирект
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_comment_delete_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('comment-delete', kwargs={'pk': self.comment.pk}))
        # Проверка, что удаление комментария произошло и происходит редирект
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_add_comment(self):
        self.client.login(username='testuser', password='testpass')
        comment_data = {'comment': 'This is a test comment'}
        # Отправка POST-запроса на добавление комментария
        response = self.client.post(reverse('post-detail', kwargs={'pk': self.post.pk}), data=comment_data)
        # Проверка, что редирект происходит после успешного добавления комментария
        self.assertEqual(response.status_code, 302)
        # Проверка, что комментарий был добавлен
        self.assertTrue(Comment.objects.filter(comment='This is a test comment', post=self.post).exists())

