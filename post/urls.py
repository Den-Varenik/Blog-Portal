from django.conf.urls import url
from post import views

urlpatterns = [
    url(r'^like/(?P<post_slug>.+)/$', views.LikeView.as_view(), name="post-like"),
    url(r'^create/$', views.PostCreateView.as_view(), name="post-create"),
    url(r'^(?P<post_slug>.+)/update/$', views.PostUpdateView.as_view(), name="post-update"),
    url(r'^(?P<post_slug>.+)/delete/$', views.PostDeleteView.as_view(), name="post-delete"),
    url(r'^(?P<post_slug>.+)/$', views.PostDetailView.as_view(), name="post-detail"),
]
