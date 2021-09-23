import os

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from model_utils import FieldTracker


class Category(models.Model):
    name = models.CharField(_('Category'), max_length=200)
    slug = models.SlugField(_("Slug"), unique=True)

    def __str__(self) -> str:
        return str(self.name)

    def get_absolute_url(self) -> str:
        return reverse('post:post-list', args=[self.slug])


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(_("Title"), max_length=50)
    slug = models.SlugField(_("Slug"), unique=True)
    body = models.TextField(_("Text"))
    category = models.ForeignKey(Category, related_name="post", on_delete=models.CASCADE)
    img = models.FileField(upload_to="post_img/", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    tracker = FieldTracker()

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return str(self.title)

    def get_absolute_url(self) -> str:
        return reverse('post:post-detail', args=[self.category.slug, self.slug])


@receiver(models.signals.post_delete, sender=Post)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.img:
        if os.path.isfile(instance.img.path):
            os.remove(instance.img.path)
