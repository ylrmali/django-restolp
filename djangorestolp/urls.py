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

urlpatterns = [
    path('mlp/', include('modelpermission.urls')),
    path('olp/', include('objectpermission.urls'))
]
