# blog/urls.py
from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    CommentDeleteView
)
from . import views
from .views import blog_search

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('home/', views.home, name='blog-home-alt'),
    path('myblog/', PostListView.as_view(), name='blog-myblog'),
    path('about/', views.about, name='blog-about'),
    path('courses/', views.courses, name='blog-courses'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('search/', blog_search, name='blog_search'),

]
