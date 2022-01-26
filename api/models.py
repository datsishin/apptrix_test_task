from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=200, verbose_name='Имя пользователя')
    last_name = models.CharField(max_length=200, verbose_name='Фамилия пользователя')
    gender_choices = [
        ('М', 'Мужчина'),
        ('Ж', 'Женщина')
    ]
    gender = models.CharField(max_length=1, verbose_name='Пол пользователя', choices=gender_choices, default='М')
    avatar = models.ImageField(verbose_name='Аватар пользователя', upload_to='avatars/%Y/%m/%d/', null=True, blank=True)
    email = models.EmailField(max_length=254)
    lon = models.DecimalField(verbose_name='Долгота местонахождения пользователя', max_digits=8,
                              decimal_places=6, null=True, blank=True)
    lat = models.DecimalField(verbose_name='Широта местонахождения пользователя', max_digits=8,
                              decimal_places=6, null=True, blank=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')

    class Meta:
        unique_together = ['user', 'follower']
