# blog/views.py

from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post, Category
from .models import Comment
from .forms import CommentForm, PostForm
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Q

def myblog(request):
    category_id = request.GET.get('category')
    if category_id:
        posts = Post.objects.filter(categories__id=category_id)
    else:
        posts = Post.objects.all()

    categories = Category.objects.all()

    context = {
        'posts': posts,
        'categories': categories,
        'title': 'Блог',
        'active_page':'myblog',
    }
    return render(request, 'blog/myblog.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/myblog.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        category_id = self.request.GET.get('category')
        if category_id:
            return Post.objects.filter(categories__id=category_id).order_by('-date_posted')
        return Post.objects.all().order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'myblog'
        context['categories'] = Category.objects.all()
        return context

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.filter(
            parent_comment=None).all()  # Получаем только корневые комментарии
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.user = request.user
            parent_id = request.POST.get('parent_id')  # Получаем идентификатор родительского комментария, если он есть
            if parent_id:
                comment.parent_comment = Comment.objects.get(id=parent_id)
            comment.save()
            return redirect(self.object.get_absolute_url())
        return self.render_to_response(self.get_context_data(comment_form=form))


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        # Проверка на разрешение создания постов
        if not self.request.user.profile.can_create_posts:
            return redirect('blog-myblog')

        form.instance.author = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        # Если форма недействительна, возвращаем тот же шаблон с формой и ошибками
        return self.render_to_response(self.get_context_data(form=form))  # Отображаем ошибки формы

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user


def home(request):
    context={
        'MEDIA_URL': settings.MEDIA_URL,
        'title':'Главная',
        'active_page':'home',
    }
    return render(request, 'blog/home.html', context)


def about(request):
    context={
        'MEDIA_URL': settings.MEDIA_URL,
        'title':'О проекте',
        'active_page':'about',
    }
    return render(request, 'blog/about.html', context)

def courses(request):
    context={
        'MEDIA_URL': settings.MEDIA_URL,
        'title':'Тарифы',
        'active_page':'courses',
    }
    return render(request, 'blog/courses.html', context)


def blog_search(request):
    query = request.GET.get('query', '')
    # Используем Q для создания условия "или", чтобы искать по заголовку или содержимому
    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    )
    results = []

    for post in posts:
        results.append({
            'id': post.id,
            'title': post.title,
            'content': post.content[:100],  # Добавляем краткий текст, если необходимо
            'date_posted': post.date_posted.strftime('%B %d, %Y'),
            'author': post.author.username,
            'author_profile': post.author.profile.image.url,  # URL изображения автора
        })

    return JsonResponse({'posts': results})
