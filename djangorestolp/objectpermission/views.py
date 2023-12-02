from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    DjangoModelPermissions,
    DjangoObjectPermissions)
from objectpermission.serializer import (
    ObjectLevelUserSerializer,
    ObjectLevelGroupSerializer)
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView)
from django.contrib.auth.models import (
    Permission,
    Group)
from objectpermission.utils import (
    UserObjectLevelPermission,
    GroupObjectLevelPermission)
from django.contrib.auth import get_user_model
from objectpermission.utils import Validators

# Create your views here.

def validate_form_data(*args, **kwargs):
    '''
    Validate form data
    '''
    response = {}
    if kwargs.get('group') is None and not kwargs.get('user'):
        response['user'] = 'User is required'
    elif kwargs.get('group') is None and kwargs.get('user'):
        if Validators().is_user_exist(user=kwargs.get('user')) == False: 
            response['user'] = "User is not found"

    if  kwargs.get('user') is None and not kwargs.get('group'):
        response['group'] = 'Group is required'
    elif kwargs.get('user') is None and kwargs.get('group'):
        if Validators().is_group_exist(group=kwargs.get('group')) == False:
            response['group'] = 'Group is not found'

    if not kwargs.get('permission'):
        response['permission'] = 'Permission is required'
    else:
        if Validators().is_permission_range(
            permission=int(kwargs.get('permission'))) == False:
            response['permission'] = 'Permission level should be 1, 2, 3 or 4'
    
    if not kwargs.get('model_name'):
        response['model_name'] = 'Model name is required'
    else:
        if Validators().is_model_exist(
            app_label=kwargs.get('app_label'),
            model=kwargs.get('model_name')) == False:
            response['model_name'] = 'Model name not found'

    if not kwargs.get('app_label'):
        response['app_label'] = 'App label is required'
    else:
        if Validators().is_app_label_exist(app_label=kwargs.get('app_label')) == False:
            response['app_label'] = 'App label not found'
    
    if not kwargs.get('object_id'):
        response['object_id'] = 'Object id is required'
    else:
        if Validators().is_object_exist(
            app_label=kwargs.get('app_label'),
            model=kwargs.get('model_name'),
            object_id=int(kwargs.get('object_id'))) == False:
            response['object_id'] = 'Object id not found'
    
    return response if response != {} else True
    

class ObjectLevelUserPermissions(ListAPIView, CreateAPIView):
    '''
    List of user permissions and create new permission
    Just for admin user can access
    '''
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ObjectLevelUserSerializer
    
    def get(self, request, *args, **kwargs):
        permissions = UserObjectLevelPermission().get_all_user_permissions()
        return Response(permissions)
    
    def post(self, request, *args, **kwargs):
        user = int(request.data.get('user'))
        permission_level = request.data.get('permission_level')
        model_name = request.data.get('model_name')
        app_label = request.data.get('app_label')
        object_id = request.data.get('object')
        # Validate form data
        response = validate_form_data(
            user=user, 
            permission=permission_level,
            model_name=model_name,
            app_label=app_label,
            object_id=object_id
        )
        if response == True:
            # convert to object 
            perm = UserObjectLevelPermission()
            model = perm._get_model(
                app_label=app_label,
                model=model_name)
            obj = perm._get_object(
                model=model,
                object_id=object_id)
            user = get_user_model().objects.get(id=user)

            # Create new permission
            perm.set_object_level_permissions(
                model=model,
                obj=obj,
                user=user,
                permission_level=int(permission_level)
            )
            
            return Response(
                data={
                    'message': 'Create new permission successfully'
                },
                status=201
            )
        else:
            return Response(data=response, status=400)

class ObjectLevelGroupPermissions(ListAPIView, CreateAPIView):
    '''
    List of user permissions and create new permission
    Just for admin user can access
    '''
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ObjectLevelGroupSerializer

    def get(self, request, *args, **kwargs):
        permissions = GroupObjectLevelPermission().get_all_group_permissions()
        return Response(permissions)
    
    def post(self, request, *args, **kwargs):
        group = int(request.data.get('group'))
        permission_level = request.data.get('permission_level')
        model_name = request.data.get('model_name')
        app_label = request.data.get('app_label')
        object_id = request.data.get('object')
        # Validate form data
        response = validate_form_data(
            group=group, 
            permission=permission_level,
            model_name=model_name,
            app_label=app_label,
            object_id=object_id
        )

        if response == True:
            # convert to object 
            perm = GroupObjectLevelPermission()
            model = perm._get_model(
                app_label=app_label,
                model=model_name)
            obj = perm._get_object(
                model=model,
                object_id=object_id)
            group = Group.objects.get(id=group)

            # # Create new permission
            perm.set_object_level_permissions(
                model=model,
                obj=obj,
                group=group,
                permission_level=int(permission_level)
            )
            
            return Response(
                data={
                    'message': 'Create new permission successfully'
                },
                status=201
            )
        else:
            return Response(data=response, status=400)
