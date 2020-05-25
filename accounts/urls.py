from django.urls import path, re_path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    re_path(r'^dashboard/(?P<parameter>[\w-]+).html', views.dash_content, name="dash_content")
]