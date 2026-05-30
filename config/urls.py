from django.contrib import admin
from django.urls import (
    path,
    include
)

urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),

    path(
        'api/users/',
        include('users.urls')
    ),

    path(
        'api/business/',
        include('business.urls')
    ),
    path(
     'api/access-control/',
        include(
            'access_control.urls'
     )
    ),
]
