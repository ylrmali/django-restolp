"""
URL configuration for django-restolp library.
Should be included in the project's main URL configuration file.

Author: Ali Yıldırım <ylrmali1289@gmail.com> (
    github.com/ylrmali,
    linkedin.com/in/ylrmali
)
"""
from django.urls import path, include
from django.conf import settings

urlpatterns = []

if settings.INSTALLED_APPS.__contains__('modelpermission'):
    urlpatterns.append(
        path('mlp/', include('modelpermission.urls'))
    )
if settings.INSTALLED_APPS.__contains__('objectpermission'):
    urlpatterns.append(
        path('olp/', include('objectpermission.urls'))
    )
