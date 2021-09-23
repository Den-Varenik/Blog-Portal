from django.contrib import admin
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

urlpatterns = [
    url(settings.ADMIN_URL, admin.site.urls),
    url(r"^", include(("home.urls", "home"), namespace="home")),
    url(r"^post/", include(("post.urls", "post"), namespace="post")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [url('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
