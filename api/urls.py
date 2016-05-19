from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^publications/$', views.PublicationList.as_view()),
    url(r'^publications/(?P<pk>[0-9]+)/$', views.PublicationDetail.as_view()),
    url(r'^users/self/$', views.Self.as_view()),

]

"""

/publications/
/publications/<id>/
/users/
/users/<id>/
/users/<id>/publications/
/users/self/
/users/self/publications/

"""