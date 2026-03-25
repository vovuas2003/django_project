"""
Админ-панель
"""

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, TestResult

# Регистрируем UserProfile
admin.site.register(UserProfile)

class UserProfileInline(admin.StackedInline):
    """
    Добавим профиль в админку пользователей
    """
    model = UserProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    """
    Расширяем стандартный UserAdmin
    """
    inlines = (UserProfileInline,)

# Отменяем регистрацию стандартного User и регистрируем кастомный
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    """
    Регистрируем модель TestResult в админке
    """
    list_display = ('user', 'score', 'total_time_seconds', 'started_at', 'is_perfect')
    list_filter = ('score', 'started_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('started_at',)
    ordering = ('-started_at',)
    def is_perfect(self, obj):
        """
        Идеальный тест - 10/10
        """
        return obj.is_perfect()
    is_perfect.boolean = True
    is_perfect.short_description = 'Идеальный результат'
