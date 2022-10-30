from django.contrib import admin
from .models import blog_data, blog_classification

# Register your models here.
admin.site.register(blog_data)
admin.site.register(blog_classification)