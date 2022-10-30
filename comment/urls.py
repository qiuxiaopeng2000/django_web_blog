from django.urls import path
# 引入views.py
from . import views

urlpatterns = [
    path('comment-to-blog/<int:blog_id>/', views.create_comment, name="comment_to_blog"),
    path('comment-to-user/<int:blog_id>/<int:user_id>/', views.create_comment, name="comment_to_user"),
    path('blog-delete/<int:id>/', views.delete_comment, name="delete_comment"),
]