from django.urls import path
from . import views

app_name = 'loginmanager'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('login_result/', views.login_result, name='login_result'),
    path('logout/', views.logout_result, name='logout'),
    path('signup/', views.signup_view, name='register'),
    path('signup_result/', views.signup_result, name='register_result'),
    path('modify_profile/', views.modify_profile_view, name='modify_profile'),
    path('modify_profile_result/', views.modify_profile_result, name='modify_profile_result'),
]