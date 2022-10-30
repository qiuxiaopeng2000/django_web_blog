from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
from django.utils import timezone
from taggit.managers import TaggableManager


# 文章类别
class blog_classification(models.Model):
    name = models.CharField(max_length=50, blank=True)
    created_time = models.DateTimeField(default=timezone.now)


# 文章内容
class blog_data(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = RichTextField()
    classification = models.ForeignKey(blog_classification, blank=True, null=True, on_delete=models.CASCADE, related_name="blog_class")
    num_of_views = models.IntegerField(default=0)
    num_of_likes = models.IntegerField(default=0)
    num_of_comments = models.IntegerField(default=0)
    created_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(auto_now=True)
    is_original = models.BooleanField(default=False)
    tags = TaggableManager(blank=True)
    from_author = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)


    class Meta:
        ordering = ('-created_time',)
