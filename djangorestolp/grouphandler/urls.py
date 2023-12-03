from django.urls import path
from djangorestolp.grouphandler.views import (
    GroupViewset,
)
from rest_framework import routers

app_name = 'grouphandler'
router = routers.SimpleRouter()
router.register('', GroupViewset, basename='group')
urlpatterns = router.urls
