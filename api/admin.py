from django.contrib import admin

from .models import CustomUser, Like


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name',)
    search_fields = ("first_name",)
    list_filter = ("first_name",)
    empty_value_display = '-пусто-'


class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'follower',)
    search_fields = ('user', 'follower',)
    list_filter = ('user', 'follower',)
    empty_value_display = '-пусто-'


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Like, LikeAdmin)
