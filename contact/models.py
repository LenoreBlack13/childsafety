# conatct/models.py

from django.db import models
from django.utils import timezone

class Contact(models.Model):
    PROJECT_CHOICES = [
        ('child-center', 'Занятие с детьми в детском центре'),
        ('other', 'Индивидуальное занятие'),
        ('marathon', 'Марафон по безопасности'),
        ('training', 'Тренинг для родителей'),
    ]
    name = models.CharField(max_length=100, verbose_name='Ваше имя')
    phone = models.CharField(max_length=20, verbose_name='Ваш номер телефона')
    email = models.EmailField(max_length=255, verbose_name='Ваш email')
    project = models.CharField(max_length=50, choices=PROJECT_CHOICES, verbose_name='Выберите направление')
    create_at = models.DateTimeField(default=timezone.now, verbose_name='Дата заявки')

    def __str__(self):
        return f'{self.name} - {self.project}'