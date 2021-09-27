from django.contrib import admin
from post.models import Category, Post, Author

admin.site.register((Category, Post, Author,))
