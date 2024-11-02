# review/models.py

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse

class Review(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    rating=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review=models.TextField()
    date_posted=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Отзыв от {self.user.username}'