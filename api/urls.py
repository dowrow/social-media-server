from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^publications/$', views.PublicationList.as_view()), # /publications/
    url(r'^publications/(?P<pk>[0-9]+)/$', views.PublicationDetail.as_view()), # /publications/{id}/
    url(r'^users/self/$', views.SelfDetail.as_view()), # /users/self/
    url(r'^users/self/publications/$', views.SelfPublicationList.as_view()),  # /users/self/publications/
    url(r'^users/(?P<pk>[0-9]+)/publications/', views.UserPublicationList.as_view()),  # /users/{id}/publications/

    # url(r'^users/(?P<pk>[0-9]+)/', views.UserDetail.as_view()), # /users/{id}/
    # url(r'^users/(?P<pk>[0-9]+)/', views.UserDetail.as_view()), # /users/{id}/
]

"""

/publications/ -
/publications/<id>/ -
/users/
/users/<id>/
/users/<id>/publications/ -
/users/self/ -
/users/self/publications/ -

"""