from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=200, verbose_name='Имя пользователя')
    second_name = models.CharField(max_length=200, verbose_name='Фамилия пользователя')
    gender_choices = [
        ('М', 'Мужчина'),
        ('Ж', 'Женщина')
    ]
    gender = models.CharField(max_length=1, verbose_name='Пол пользователя', choices=gender_choices, default='М')
    avatar = models.ImageField(verbose_name='Аватар пользователя')
    email = models.EmailField(max_length=254)