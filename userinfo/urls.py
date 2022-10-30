from django.urls import path
# 引入views.py
from . import views


urlpatterns = [
    path('login/', views.user_login, name="user_login"),
    path('logout/', views.user_logout, name="user_logout"),
    path('register/', views.user_register, name="user_register"),
    path('user-info-edit/<int:user_id>/', views.user_info_edit, name='user_info_edit'),
    path('user-delete/<int:user_id>/', views.user_delete, name='user_delete'),
    path('change-password/<int:user_id>/', views.change_password, name="change_password"),
    path('follow-orther/<int:user_id1>/<int:user_id2>/<int:blog_id>/', views.follow_other, name="follow_other"),
    path('my-follow/<int:user_id>/', views.my_follow, name='my_follow'),
    path('my-fans/<int:user_id>/', views.my_fans, name='my_fans'),
]