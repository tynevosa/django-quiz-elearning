from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'quiz'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('', views.testmath, name='testmath'),
]
