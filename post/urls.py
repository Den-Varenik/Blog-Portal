from django.conf.urls import url
from post import views

urlpatterns = [
    url(r'^create/$', views.PostCreateView.as_view(), name="post-create"),
    url(r'^(?P<post_slug>.+)/update/$', views.PostUpdateView.as_view(), name="post-update"),
    url(r'^(?P<post_slug>.+)/delete/$', views.PostDeleteView.as_view(), name="post-delete"),
    url(r'^(?P<category_slug>.+)/(?P<post_slug>.+)/$', views.PostDetailView.as_view(), name="post-detail"),
    url(r'^(?P<category_slug>.+)/$', views.PostListView.as_view(), name="post-list"),
]
