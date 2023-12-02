from rest_framework import routers
from rest_framework.response import Response
from modelpermission.views import (
    HomeView,
    UserPermissions, 
    ReadOnlyUserPermission, 
    GroupPermissions)
from django.urls import path

router = routers.SimpleRouter()

urlpatterns = router.urls
urlpatterns.append(
    path(
        'user-perms/', 
        UserPermissions.as_view(), 
        name='permissions'
    )
)
urlpatterns.append(
    path(
        'read-perms/', 
        ReadOnlyUserPermission.as_view(), 
        name='user-permissions'
    )
)
urlpatterns.append(
    path(
        'group-perms/', 
        GroupPermissions.as_view(), 
        name='group-permissions'
    )
)


