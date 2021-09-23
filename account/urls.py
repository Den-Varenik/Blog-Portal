from django.conf.urls import url
from account import views

urlpatterns = [
    url(r'^login/$', views.UserLoginView.as_view(), name="login"),
    url(r'^logout/$', views.logout_user, name="logout"),
    url(r'^register/$', views.UserCreateView.as_view(), name="register"),
    # url(r'^password_change/$', views, name="change"),
    # url(r'^password_reset/$', views, name="reset"),
]
