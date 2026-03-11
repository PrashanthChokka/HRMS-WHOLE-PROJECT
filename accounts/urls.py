from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # Root opens login
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('base/', views.base_view, name='base'),   
    path('logout/', views.logout_view, name='logout'),
]