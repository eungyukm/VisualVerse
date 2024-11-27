from django.shortcuts import render
from django.urls import path, re_path
from . import views

app_name = 'postmanager'
urlpatterns = [
    path('post_list/', views.PostLV.as_view(), name='post_list'),

    # Slug 컨버터는 [a-zA-Z0-9_-] 문자열을 받아들인다.
    # re_path는 정규표현식을 사용할 수 있게 해준다.
    re_path(r'^post/(?P<pk>\d+)/$', views.PostDV.as_view(), name='post_detail'),

    path('archive/', views.PostAV.as_view(), name='post_archive'),

    path('', views.main, name='main'),
    path('post_write/', views.post_write, name='post_write'),
    path('post_write_result/', views.post_write_result, name='post_write_result'),
]