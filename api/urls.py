from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^users/$', views.UserList.as_view()),
    url(r'^me/$', views.Me.as_view()),
    url(r'^publications/$', views.PublicationList.as_view()),
    url(r'^publications/(?P<pk>[0-9]+)/$', views.PublicationDetail.as_view()),
]