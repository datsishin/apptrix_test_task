from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from imagekit.models import ProcessedImageField

from dating_app.dating_app.settings import MEDIA_AVATARS_DIR
from .processors import Watermark


class CustomManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('User must have an email!')
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.password = make_password(password)
        user.is_active = True
        user.is_staff = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.password = make_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=200, verbose_name='Имя пользователя')
    last_name = models.CharField(max_length=200, verbose_name='Фамилия пользователя')
    gender_choices = [
        ('М', 'Мужчина'),
        ('Ж', 'Женщина')
    ]
    gender = models.CharField(max_length=1, verbose_name='Пол пользователя', choices=gender_choices, default='М')
    avatar = ProcessedImageField(verbose_name='Аватар пользователя', processors=[Watermark()],
                                 upload_to=MEDIA_AVATARS_DIR, null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=50, unique=True, blank=False)
    lon = models.DecimalField(verbose_name='Долгота местонахождения пользователя', max_digits=8,
                              decimal_places=6, null=True, blank=True)
    lat = models.DecimalField(verbose_name='Широта местонахождения пользователя', max_digits=8,
                              decimal_places=6, null=True, blank=True)

    objects = CustomManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='follower')

    class Meta:
        unique_together = ['user', 'follower']
