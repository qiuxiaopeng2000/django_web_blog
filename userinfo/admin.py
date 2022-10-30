from django.contrib import admin

# Register your models here.
from .models import user_info_data, Follow

admin.site.register(user_info_data)
admin.site.register(Follow)
