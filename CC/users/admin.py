from django.contrib import admin
from .models import CoffeeUsers, OtdelClass
from django.contrib.auth.models import Group

@admin.register(CoffeeUsers)
class UsersAdmin(admin.ModelAdmin):
    model = CoffeeUsers
    list_display = ('id', 'username', 'chat_id', 'first_name', 'last_name', 'middle_name', 'birth_day', 'phone', 'email', 'otdel', 'position', 'avatar', 'nachalnik', 'is_staff', 'is_active')
    list_filter = ('is_active', 'is_staff', 'otdel', 'nachalnik')
    search_fields = ('email', 'phone', 'otdel', 'position')
    exclude = ('password', 'last_login', 'groups', 'user_permissions')


@admin.register(OtdelClass)
class OtdelAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title',)
    search_fields = ('title',)

admin.site.unregister(Group)
