from django.contrib import admin
from django.conf import settings
from django.conf.urls import url, include

urlpatterns = [
    url(settings.ADMIN_URL, admin.site.urls),
    url(r"^", include(("home.urls", "home"), namespace="home")),
    url(r"^post/", include(("post.urls", "post"), namespace="post")),
]
