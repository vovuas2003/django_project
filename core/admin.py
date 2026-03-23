from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, TestResult

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

# Регистрируем модель TestResult в админке
@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
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
