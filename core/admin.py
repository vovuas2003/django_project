from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile

# Регистрируем UserProfile
admin.site.register(UserProfile)

# Дополнительно: добавим профиль в админку пользователей
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

# Отменяем регистрацию стандартного User и регистрируем кастомный
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
