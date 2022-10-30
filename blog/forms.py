from django import forms
from .models import blog_data


# 新建文章的提交数据
class blog_create_form(forms.ModelForm):
    class Meta:
        model = blog_data
        fields = ('title', 'body', 'tags')
