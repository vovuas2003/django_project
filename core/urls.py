"""
Соответствие ссылок и функций-обработчиков
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('password_change/', views.password_change, name='password_change'),
    path('password_change/done/', views.password_change, name='password_change_done'),
    path('test/start/', views.start_test, name='start_test'),
    path('test/submit/', views.submit_test, name='submit_test'),
    path('test/results/', views.test_results, name='test_results'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('perfect-trend/', views.perfect_trend, name='perfect_trend'),
    path('results/', views.test_results, name='test_results'),
    path('results/<int:test_id>/', views.test_detail, name='test_detail'),
]
