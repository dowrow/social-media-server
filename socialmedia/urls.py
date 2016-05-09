from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    url(r'^api/v0/', include('api.urls')),
]

""""""
""""""
