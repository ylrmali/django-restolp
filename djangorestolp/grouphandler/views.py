from rest_framework.generics import (
    ListAPIView, 
    RetrieveAPIView, 
    CreateAPIView, 
    UpdateAPIView, 
    DestroyAPIView
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from djangorestolp.grouphandler.serializer import GroupSerializer
from django.contrib.auth.models import Group
from djangorestolp.modelpermission.utils import GroupModelLevelPermission
from django.contrib.auth import get_user_model
from djangorestolp.grouphandler.utils import GroupWithUser
from django.db.models import Q


class GroupViewset(ModelViewSet):
    """
    List all groups, or create a new group.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = GroupSerializer
    queryset = Group.objects.all()


    def return_response(self, serializer, status=status.HTTP_201_CREATED):
        """
        Return response.
        """
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status, headers=headers)

    def create(self, request, *args, **kwargs):
        """
        Overrited create method
        This method will create new group but,
        if you want you can assign group to user
        """
        user = request.data.getlist('user')
        group = request.data.get('name')
        serializer = self.return_response(serializer=self.get_serializer(data=request.data))
        if user is not None:
            try:
                # conver string user id to int
                user = [int(u) for u in user]
                # assign group to user
                group_perms = GroupModelLevelPermission()
                if len(user) >= 1:
                    for u in user:
                        group_perms.create_group_or_assgin_user(
                            group=group,
                            user=get_user_model().objects.get(id=u),
                            both=True
                        )
                else:
                    group_perms.create_group_or_assgin_user(
                        group=group
                    )
                
                return Response(data=serializer.data)
            except Exception as e:
                return Response(
                    {'error': str(e), 'suceess': 'Group created but user not assigned.'},  
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            # if is user is None just create group
            group_perms.create_group_or_assgin_user(group=group)
            return Response(data=serializer.data)

    def list(self, request, *args, **kwargs):
        """
        Override list method.
        Return a list of all groups.
        This method provide a list of users in a group.
        """
        queryset = GroupWithUser().get_group_with_user()
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        Override retrieve method.
        Return a group instance.
        This method provide a list of users in a group.
        """
        pk_value = int(kwargs['pk'])

        queryset = GroupWithUser().get_group_detail_with_user(pk_value)
        serializer = self.get_serializer(queryset)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        """
        Override update method.
        This method use django-restolp method to update 
        """
        group_perms = GroupModelLevelPermission()
        # control group name is same or not
        if request.data.get('name') == Group.objects.get(id=kwargs['pk']).name:
            pass
        else:
            # if group name change, save new group name to db
            group = Group.objects.get(id=kwargs['pk'])
            group.name = request.data.get('name')
            group.save()


        if request.data.getlist('user') is not None:
            # conver string user id to int
            user = [int(u) for u in request.data.getlist('user')]
            # assign group to user
            if len(user) >= 1:
                group_obj = Group.objects.get(id=kwargs['pk'])
                group_perms.remove_group_from_user(group=group_obj) # first remove old data 
                for u in user:
                    group_perms.create_group_or_assgin_user(
                        group=group_obj,
                        user=get_user_model().objects.get(id=u),
                    )
            else:
                group_perms.remove_group_from_user(
                    group=Group.objects.get(id=kwargs['pk'])
                )

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # we call the object with `get_serializer` method, 
        # so we can not return user list
        # because Group object has no user field in model 
        # we created our dictionary data to show update result.
        updated_data = serializer.data.copy()  # Make a copy to avoid modifying the original data
        updated_data['user'] = [int(u) for u in request.data.getlist('user')]

        # Return the modified data
        return Response(data=updated_data, status=status.HTTP_200_OK)
        
    def partial_update(self, request, *args, **kwargs):
        """
        Override partial_update method.
        Return a group instance.
        This method provide a list of users in a group.
        """
        group_perms = GroupModelLevelPermission()
        group = Group.objects.get(id=kwargs['pk'])
        prev_name = group.name
        prev_user = [user.username for user in get_user_model().objects.all()\
                      if user.groups.filter(name=prev_name).exists()]
        if request.data.get('name') != '' and request.data.get('name') != prev_name:
            group.name = request.data.get('name')
            group.save()
        if request.data.get('user') is not None or request.data.get('user') != prev_user:
            user = [int(u) for u in request.data.get('user')]
            if len(user) >= 1:
                for u in user:
                    group_perms.create_group_or_assgin_user(
                        group=group,
                        user=get_user_model().objects.get(id=u),
                    )
            else:
                group_perms.remove_group_from_user(
                    group=group
                )

        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        # we call the object with `get_serializer` method, 
        # so we can not return user list
        # because Group object has no user field in model 
        # we created our dictionary data to show update result.
        updated_data = serializer.data.copy()  # Make a copy to avoid modifying the original data
        updated_data['user'] = [int(u) for u in request.data.get('user')]

        # there is a problem with after update no input user field choose
        return Response(data=updated_data, status=status.HTTP_200_OK)


