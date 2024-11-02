# review/urls.py

from django.urls import path
from .views import (
    ReviewListView,
    ReviewUpdateView,
    ReviewDeleteView
)

urlpatterns = [
    path('', ReviewListView.as_view(), name='review-reviews'),
    path('review/<int:pk>/update/', ReviewUpdateView.as_view(), name='review-update'),
    path('review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
]