import os

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from model_utils import FieldTracker


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alias = models.CharField(_("Alias"), max_length=50)
    first_name = models.CharField(_("Name"), max_length=50, null=True, blank=True)
    second_name = models.CharField(_("Surname"), max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.alias)


class Category(models.Model):
    name = models.CharField(_('Category'), max_length=200)
    slug = models.SlugField(_("Slug"), unique=True)

    def __str__(self) -> str:
        return str(self.name)

    def get_absolute_url(self) -> str:
        return reverse('home:post-list', args=[self.slug])


class Post(models.Model):
    author = models.ForeignKey(Author, related_name="post", on_delete=models.CASCADE)
    title = models.CharField(_("Title"), max_length=50)
    slug = models.SlugField(_("Slug"), unique=True)
    body = models.TextField(_("Text"))
    category = models.ForeignKey(Category, related_name="posts", on_delete=models.CASCADE)
    img = models.FileField(upload_to="post_img/", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    tracker = FieldTracker()

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return str(self.title)

    def get_absolute_url(self) -> str:
        return reverse('post:post-detail', args=[self.slug])

    def get_absolute_url_to_like(self) -> str:
        return reverse('post:post-like',  args=[self.slug])


@receiver(models.signals.post_delete, sender=Post)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.img:
        if os.path.isfile(instance.img.path):
            os.remove(instance.img.path)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comment", on_delete=models.CASCADE)
    text = models.TextField(_("Comment"))
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="like", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self) -> str:
        return reverse('post:post-like')
