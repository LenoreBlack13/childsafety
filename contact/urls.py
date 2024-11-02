# contact/urls.py
from django.urls import path
from django.views.generic import TemplateView  # Импортируйте TemplateView
from .views import contact_view

urlpatterns = [
    path('', contact_view, name='contact-contact'),
    path('contact_send_success/', TemplateView.as_view(template_name='contact/contact_send_success.html'), name='contact_send_success'),
]