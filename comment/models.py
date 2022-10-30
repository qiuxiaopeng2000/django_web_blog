from django.db import models
from django.contrib.auth.models import User
from blog.models import blog_data
# django-ckeditor
from ckeditor.fields import RichTextField
# django-mptt
from mptt.models import MPTTModel, TreeForeignKey


# 博文的评论
class comment_data(MPTTModel):
    article = models.ForeignKey(
        blog_data,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    comment_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    # mptt树形结构
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    # 记录二级评论回复给谁, str
    reply_to_obj = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='repliers'
    )

    body = RichTextField()
    created_time = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['created_time']

