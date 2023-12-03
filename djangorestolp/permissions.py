from rest_framework import permissions

class DROPermission(permissions.BasePermission):
    '''
    Custom permission class for Django Rest Object.
    This class is used to check object-level permissions.
    '''
    def get_permission_name(self, action, model_name):
        '''
        Returns permission name for the given action and model name.
        '''
        return f"{action}_{model_name.lower()}"
    
    def convert_action(self, action):
        '''
        Converts action name to permission name.
        '''
        action_map = {
            'list': 'view',
            'retrieve': 'view',
            'create': 'add',
            'update': 'change',
            'partial_update': 'change',
            'destroy': 'delete'
        }
        return action_map.get(action)
    
    def has_permission(self, request, view):
        '''
        Check user has permission on the given model.
        '''
        return request.user.has_perm(f'{view.get_app_label()}.view_{view.get_model_name()}')

    def has_object_permission(self, request, view, obj):
        '''
        Check user has permission on the given object.
        '''
        model_name = type(obj).__name__
        action = self.convert_action(view.action)
        required_permission = self.get_permission_name(action, model_name)

        return required_permission in request.user.get_all_permissions(obj)