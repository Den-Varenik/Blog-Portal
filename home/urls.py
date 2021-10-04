from django.conf.urls import url
from home import views

urlpatterns = [
    url(r'^$', views.CategoryListView.as_view(), name="category-list"),
    url(r'^follow/(?P<category_slug>.+)/$', views.PostListView.as_view(), name="post-list"),
]
