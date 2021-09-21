from django.contrib import admin
from post.models import Category, Post

admin.site.register([Category, Post])
