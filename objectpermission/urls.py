from rest_framework import routers
from objectpermission.views import (
    ObjectLevelUserPermissions,
    ObjectLevelGroupPermissions,
)
from django.urls import path

router = routers.SimpleRouter()

urlpatterns = router.urls
urlpatterns.append(
    path(
        'user-perms/', 
        ObjectLevelUserPermissions.as_view(), 
        name='user-permissions'
    )
)
urlpatterns.append(
    path(
        'group-perms/', 
        ObjectLevelGroupPermissions.as_view(), 
        name='group-permissions'
    )
)
