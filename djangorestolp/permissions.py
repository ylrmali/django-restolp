from rest_framework.permissions import DjangoObjectPermissions, DjangoModelPermission
from djangorestolp.settings import api_settings


class DROPermission(DjangoObjectPermissions):
    """
    Override DjangoObjectPermission class to permission map 
    and optinal user configurations
    """
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


    def _check_bypass_user(self, user : object, user_arr : list) -> bool:
        """
        Check user bypass configuration and return true or false
        """
        if len(user_arr) <= 0:
            # if bypass user is not set, return False
            return False

        if user.username in user_arr:
            # if requested user is member of bypass_user list, return True
            return True

        return False


    def _check_bypass_group(self, user : object, group_arr : list) -> bool:
        """
        Check group bypass configuration and return true or false
        """
        if len(group_arr) <= 0:
            # if bypass group is not set, return False
            return False

        if user.groups.filter(name__in=group_arr).count() > 0:
            # if user member of the bypass group(s), return True
            return True

        return False


    def has_object_permission(self, request, view, obj):
        user = request.user
        dro_conf = api_setting.DRO_CONF  # Access user-configured setting
        try:
            bypass_staff = dro_conf['BYPASS_STAFF_USER']
            bypass_group = dro_conf['BYPASS_GROUP_LIST']
            bypass_user = dro_conf['BYPASS_USER_LIST']
        except KeyError as e:
            raise e

        if bypass_staff and user.is_staff:  
            # if user is staff, give permission
            return True

        if self._check_bypass_user(user=user, user_arr=bypass_user):
            # if user in the bypass user list, give permission
            return True

        if self._check_bypass_group(user=user, group_arr=bypass_group):
            # if user member of bypass group, give permission
            return True

        return super().has_object_permission(request, view, obj)

    
class DROModelPermission(permissions.DjangoModelPermissions):
    '''
    Override DjangoModelPermissions to check extra view permissions.
    '''
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
