from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.LoginAPI.as_view()),
    url(r'^register/$', views.RegisterAPI.as_view()),
    url(r'^contacts/$', views.ContactsAPI.as_view()),
    url(r'^logout/$', views.LogoutAPI.as_view())
]