from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated, 
    IsAdminUser,
    DjangoModelPermissions, 
    DjangoObjectPermissions) 
from modelpermission.serializer import (
    PermissionSerializer, 
    GroupPermissionSerializer)
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView, 
    RetrieveAPIView, 
    UpdateAPIView, 
    DestroyAPIView)
from django.contrib.auth.models import (
    Permission, 
    Group)
from modelpermission.utils import (
    UserModelLevelPermissions, 
    GroupModelLevelPermission)
from objectpermission.utils import (
    BaseObjectLevelPermission, 
    UserObjectLevelPermission, 
    GroupObjectLevelPermission)
from modelpermission import urls


class HomeView(ListAPIView):
    '''
    Home page of API
    '''
    permission_classes = [AllowAny]
    serializer_class = PermissionSerializer

    def get(self, request, *args, **kwargs):
        path = [p for p in urls.urlpatterns]
        print(path)
        return Response({'message': 'Welcome to Django Easy Perm Library API'})
        

class ReadOnlyUserPermission(ListAPIView):
    '''
    List of requested user permissions
    '''
    permission_classes = [IsAuthenticated]
    serializer_class = PermissionSerializer

    def get(self, request, *args, **kwargs):
        permissions = UserModelLevelPermissions().get_user_permissions(request.user)
        return Response(permissions)


class UserPermissions(ListAPIView, CreateAPIView):
    '''
    List of user permissions and create new permission
    Just for admin user can access
    '''
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = PermissionSerializer

    def get(self, request, *args, **kwargs):
        permissions = UserModelLevelPermissions().get_all_user_permissions()
        return Response(permissions)
    
    def post(self, request, *args, **kwargs):
        user = int(request.data.get('user'))
        permission = request.data.getlist('user_permissions')
        try:
            perms = UserModelLevelPermissions().set_user_permission_api(user, permission)
        except Exception as e:
            return Response({'error': str(e)})
        
        return Response({
            'user': get_user_model().objects.get(id=user).username,
            'permission': perms
        })
        
    
class GroupPermissions(ListAPIView, CreateAPIView):
    '''
    List of group permissions and create new permission
    Just for admin user can access
    '''
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = GroupPermissionSerializer

    def get(self, request, *args, **kwargs):
        permissions = GroupModelLevelPermission().get_all_group_permissions()
        return Response(permissions)
    
    def post(self, request, *args, **kwargs):
        group = int(request.data.get('group'))
        permission = request.data.getlist('permissions')
        print(group, permission)
        try:
            perms = GroupModelLevelPermission().set_group_permission_api(group, permission)
        except Exception as e:
            return Response({'error': str(e)})
        
        return Response({
            'group': Group.objects.get(id=group).name,
            'permission': perms
        })
    

    
        

    
