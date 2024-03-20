from rest_framework.viewsets import ModelViewSet
from djangorestolp.permissions import DROPermission
from guardian.shortcuts import get_objects_for_user




class DROViewSet(ModelViewSet):
    '''
    Base viewset class for Django Rest Object.
    This class is used to check object-level permissions.
    '''
    permission_classes = [DROPermission]  # Default permission for all actions

    def get_app_label(self):
        '''
        Returns app label of the model.
        '''
        return self.queryset.model._meta.app_label

    def get_model_name(self):
        '''
        Returns model name of the model.
        '''
        return self.queryset.model.__name__.lower()

    def get_queryset(self):
        '''
        Returns filtered queryset based on object-level permissions.
        '''
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            return get_objects_for_user(self.request.user, perms=[f'view_{self.get_model_name()}'], klass=queryset)
        return queryset.none()  # Return an empty queryset if user is not authenticated
