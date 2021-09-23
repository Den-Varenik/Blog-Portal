from home.views import index
from django.conf.urls import url

urlpatterns = [
    url('^$', index, name="index"),
]
