"""
URL configuration for django-restolp library.
Should be included in the project's main URL configuration file.

Author: Ali Yıldırım <ylrmali1289@gmail.com> (
    github.com/ylrmali,
    linkedin.com/in/ylrmali
)

Example:
    urlpatterns = [
        path('', include('djangorestolp.urls')),
    ]

"""
from django.urls import path, include

app_name = 'djangorestolp'
urlpatterns = [
    path('mlp/', include('djangorestolp.modelpermission.urls')),
    path('olp/', include('djangorestolp.objectpermission.urls')),
    path('group/', include('djangorestolp.grouphandler.urls')),
]
