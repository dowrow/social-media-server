from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^publications/$', views.PublicationList.as_view()), # /publications/

    url(r'^publications/home/$', views.HomePublicationList.as_view()),  # /publications/home/

    url(r'^publications/(?P<pk>[0-9]+)/$', views.PublicationDetail.as_view()), # /publications/{id}/

    url(r'^users/$', views.UserList.as_view()), # /users/?search={search}

    url(r'^users/self/$', views.SelfDetail.as_view()), # /users/self/

    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),  # /users/{id}/

    url(r'^users/self/publications/$', views.SelfPublicationList.as_view()),  # /users/self/publications/

    url(r'^users/(?P<pk>[0-9]+)/publications/$', views.UserPublicationList.as_view()),  # /users/{id}/publications/

    url(r'^users/(?P<pk>[0-9]+)/followers/$', views.FollowUser.as_view()), # /users/{id}/followers/

    url(r'^users/(?P<followed_pk>[0-9]+)/followers/(?P<follower_pk>[0-9]+)/$', views.UnfollowUser.as_view()), # /users/{id}/followers/{id}

]
