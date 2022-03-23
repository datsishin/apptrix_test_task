from math import radians, cos

from dating_app.settings import EMAIL_HOST_USER
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import CustomUser, Like
from .serializers import UserSerializers, LikeSerializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['first_name', 'last_name', 'gender', 'lon', 'lat', ]
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        password = make_password(self.request.POST.get('password'))
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(password=password)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        if self.request.GET.get('distance'):
            distance = float(self.request.GET.get('distance'))
            user = get_object_or_404(self.queryset, id=self.request.user.id)
            my_lon = user.lon
            my_lat = user.lat
            lon1 = float(my_lon) - distance / abs(cos(radians(my_lat)) * 111.0)
            lon2 = float(my_lon) + distance / abs(cos(radians(my_lat)) * 111.0)
            lat1 = float(my_lat) - (distance / 111.0)
            lat2 = float(my_lat) + (distance / 111.0)
            queryset = CustomUser.objects.filter(lat__range=(lat1, lat2)).filter(lon__range=(lon1, lon2)).exclude(id=self.request.user.id)
            return queryset
        return self.queryset


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializers
    http_method_names = ['post']

    def create(self, request, id: int, **kwargs):
        user = CustomUser.objects.get(pk=self.request.user.id)
        follower = CustomUser.objects.get(pk=id)
        context = {'user': user, 'follower': follower, 'request': self.request}
        serializer = self.serializer_class(context=context, data=request.data)
        if serializer.is_valid():
            serializer.save()
            like_together = self.queryset.filter(user=follower)
            if like_together:
                send_mail('Сообщение с сайта знакомств!',
                          f'Вы понравились {follower.first_name}! Почта участника: {follower.email}»',
                          EMAIL_HOST_USER,
                          [user.email], fail_silently=False, )
                send_mail('Сообщение с сайта знакомств!',
                          f'Вы понравились {user.first_name}! Почта участника: {user.email}»',
                          EMAIL_HOST_USER,
                          [follower.email], fail_silently=False, )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
