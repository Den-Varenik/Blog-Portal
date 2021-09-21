from django.conf.urls import url
from post.views import PostListView, PostDetailView, PostCreateView

urlpatterns = [
    url(r'^create/$', PostCreateView.as_view(), name="post-create"),
    url(r'^(?P<category_slug>.+)/(?P<post_slug>.+)/$', PostDetailView.as_view(), name="post-detail"),
    url(r'^(?P<category_slug>.+)/$', PostListView.as_view(), name="post-list"),
]
