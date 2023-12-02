from modelpermission.utils import UserModelLevelPermissions, GroupModelLevelPermission
from objectpermission.utils import BaseObjectLevelPermission
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import get_user_model
from guardian.shortcuts import assign_perm
from django.test import TestCase
from api import models

class PermissionsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            password='test_password'
        )
        self.group = Group.objects.create(name='test_group')
        self.user_level = UserModelLevelPermissions()
        self.group_level = GroupModelLevelPermission()
        self.olp = BaseObjectLevelPermission()
        self.USER_MODEL = get_user_model()
        self.permissions_level = 1
        self.model_obj = models.Plane.objects.create(
            name='test_plane',
            color='black'
        )
        self.model_str = 'Plane'
        self.app_label = 'api'
        self.user_list = [
            "tester3",
            "tester4",
            "tester5",
            "tester6"
        ]
        # create user according to user_list
        for user in self.user_list:
            self.USER_MODEL.objects.create_user(
                username=user,
                password='test_password'
            )

    def test_set_user_permissions(self):
        '''
           test function of set user permissions
        '''
        #? test set user permissions with user object
        #* OK
        self.user_level.set_user_permission(
            user=self.user,
            permissions_level=self.permissions_level,
            model_obj=self.model_obj,
            app_label=self.app_label
        ) 

        #? test set user permissions with user list
        #* OK
        self.user_level.set_user_permission(
            user=self.user_list,
            permission_level=self.permissions_level,
            model=self.model_obj,
            app_label=self.app_label
        )

        #? test set user permissions with user string
        #* OK
        self.user_level.set_user_permission(
            user='tester3',
            permission_level=self.permissions_level,
            model=self.model_obj,
            app_label=self.app_label
        )

    def test_set_object_level_permissions(self):
        '''
            test function of set object level permissions
        '''

        #? test set object level permissions with user object
        #* OK
        self.olp.set_object_level_permissions(
            user=self.user,
            permissions_level=self.permissions_level,
            model=self.model_obj,
            app_label=self.app_label
        )