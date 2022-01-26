from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name',)
    search_fields = ("first_name",)
    list_filter = ("first_name",)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)