# test/urls.py

from django.urls import path
from .views import test_view

urlpatterns = [
    path('', test_view, name='test-test'),
]