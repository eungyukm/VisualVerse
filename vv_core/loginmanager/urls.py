from django.urls import path
from . import views

app_name = 'loginmanager'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='register'),
    path('signup_result/', views.signup_result, name='register_result'),
]