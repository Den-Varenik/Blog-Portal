from django.contrib import admin
from post.models import Category, Post, Author, Comment, Like

admin.site.register((Category, Post, Author, Comment, Like))
