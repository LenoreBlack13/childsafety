# Generated by Django 5.1.2 on 2024-10-28 17:11

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Ваше имя')),
                ('phone', models.CharField(max_length=20, verbose_name='Ваш номер телефона')),
                ('email', models.EmailField(max_length=255, verbose_name='Ваш email')),
                ('project', models.CharField(choices=[('child-center', 'Занятие с детьми в детском центре'), ('other', 'Индивидуальное занятие'), ('marathon', 'Марафон по безопасности'), ('training', 'Тренинг для родителей')], max_length=50, verbose_name='Выберите направление')),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата заявки')),
            ],
        ),
    ]
