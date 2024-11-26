from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),  # 로그인 페이지
    path('logout/', views.logout_view, name='logout'),  # 로그아웃
    path('register/', views.register_view, name='register'),  # 회원가입 페이지
]