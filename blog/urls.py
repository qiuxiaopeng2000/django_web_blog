from django.urls import path
# 引入views.py
from . import views

# app_name = 'blog'

urlpatterns = [
    path('blog-create/', views.create_blog, name="create_blog"),
    path('blog-update/<int:id>/', views.update_blog, name="update_blog"),
    path('blog-delete/<int:id>/', views.delete_blog, name="delete_blog"),
    path('blog-list/', views.blog_list, name="blog_list"),
    path('blog-list-category/<int:category_id>/', views.blog_list, name="blog_list_category"),
    path('blog-detail/<int:id>/', views.blog_detail, name='blog_detail'),
    path('blog-transmit/<int:id>/', views.transmit_blog, name='transmit_blog'),
    path('my-blog/<user>/', views.my_blog, name='my_blog'),
    # path('article-likes/<int:id>', views.increase_likes, name='article_likes'),
    path('article-likes/<int:id>', views.IncreaseLikesView.as_view(), name='article_likes'),
]
