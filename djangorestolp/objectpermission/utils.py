from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from guardian.shortcuts import assign_perm
from guardian.models import (
    UserObjectPermission,
    GroupObjectPermission)
from django.apps import apps
from djangorestolp.modelpermission.utils import BaseModelLevelPermissions
from guardian.shortcuts import remove_perm
import json

class BaseObjectLevelPermission:
    '''
    Base object level permission class
    '''
    def __init__(self):
        self.DICT = dict(result={})
        self.__ITEM = None
        self.get_permissions = BaseModelLevelPermissions().get_permissions

    def _check_parameter(
            self,
            user: str | None = None,
            group: str | None = None
        ) -> bool | ValueError:
        '''
        We should choose user or group
        If we choose both, raise ValueError
        '''
        if user is not None and group is None:
            self._set_item(user)
            return True
        elif group is not None and user is None:
            self._set_item(group)
            return True
        if user is None and group is None:
            raise ValueError("You must specify user or group")
        elif user is not None and group is not None:
            raise ValueError("You must specify user or group, not both")

    def _set_item(
            self,
            item: str   
        ) -> object:
        '''
        Get current user or group item from parameters
        '''
        self.__ITEM = item
        return self

    def _get_item(self)-> str:
        '''
        Get current user or group item from parameters
        '''
        return self.__ITEM

    def _convert_json(
            self, 
            data: dict
        ) -> json:
        '''
        Convert dict to json
        '''
        return json.dumps(data, indent=2)
    
    def _app_label_control(
            self, 
            app_label: str,
            user: str | None = None,
            group: str | None = None 
        ) -> bool:
        '''
        Check app_label is exist in result dict
        If not exist, create new app_label and return True
        '''
        if user is None and group is None:
            raise ValueError("You must specify user or group")
        elif user is not None and group is not None:
            raise ValueError("You must specify user or group, not both")
        
        if app_label not in self.DICT['result'][user if user else group]['app_label']:
            self.DICT['result'][user if user else group]['app_label'][app_label] = {"content_type": {}}
        return True
    
    def _model_and_object_control(
            self, 
            app_label: str, 
            model: object, 
            object : object,
            user: str| None = None,
            group: str | None = None 
        ) -> bool:
        '''
        Check model is exist in result dict
        If not exist, create new model and return True
        '''
        if (
            self._check_parameter(
                user=user, 
                group=group )
            and model.__name__.lower() not in self.DICT\
                ['result'][user if user else group]\
                ['app_label'][app_label]['content_type']):
            self.DICT['result'][user if user else group]\
            ['app_label'][app_label]\
            ['content_type']\
            [model.__name__.lower()] = [
                {
                    "id": object.id,
                    "permissions": []
                }
            ]
        return True

    def _get_object_index(
            self, 
            app_label: str, 
            model: object, 
            object: object,
            item: str,
            # user: str | None = None,
            # group: str | None = None 
        ) -> int:
        '''
        find object index from current model list
        '''
        for index, obj in enumerate(
            self.DICT['result'][item]\
            ['app_label'][app_label]\
            ['content_type']\
            [model.__name__.lower()]):
            if obj['id'] == object.id:
                return index
            
    def _get_object(
        self,
        model: object,
        object_id: int
        ) -> object:
        '''
        get object from app_label, model and object_id
        '''
        try:
            obj = model.objects.get(id=object_id)
            return obj
        except model.DoesNotExist as e:
            raise "Error: %s" %e

    def _get_model(
            self,
            app_label: str,
            model: str,
        ) -> object:
        '''
        get model object from app_label and model name
        '''
        if Validators().is_model_exist(app_label=app_label, model=model):
            return apps.get_model(app_label, model)
        else:
            raise ValueError("You must specify app_label and model")
        
    def _get_model_name(self, model : object) -> str:
        '''
        Get model name
        '''
        return model.__name__.lower()
    
    def _get_permission_name(
            self, 
            model : object, 
            permission_level: int
        ) -> list:
        '''
        Get permission name
        '''
        perm_map = {
            1: ["view_%s" % self._get_model_name(model=model)],
            2: ["view_%s" % self._get_model_name(model=model), 
                "add_%s" % self._get_model_name(model=model)],
            3: ["view_%s" % self._get_model_name(model=model), 
                "add_%s" % self._get_model_name(model=model), 
                "change_%s" % self._get_model_name(model=model)],
            4: ["view_%s" % self._get_model_name(model=model), 
                "add_%s" % self._get_model_name(model=model), 
                "change_%s" % self._get_model_name(model=model),
                "delete_%s" % self._get_model_name(model=model)],
        }
        return perm_map[permission_level] 
            
    def _set_permission(
            self, 
            app_label: str, 
            model: object, 
            object: object, 
            permission: str,
            user: str | None = None,
            group: str | None = None
        ) -> bool:
        '''
            get right object from dictionary
        '''
        if (self._check_parameter(
                user=user, 
                group=group
            ) and object.id not in [obj['id'] for obj in self.DICT\
                ['result'][user if user else group]['app_label']\
                [app_label]['content_type']\
                [model.__name__.lower()]]):
            # if we have not current object dict, create new dict for the object 
            self.DICT['result'][user if user else group]['app_label']\
                [app_label]['content_type'][model.__name__.lower()].append({
                    "id": object.id,
                    "permissions": []
                })
            # get object dict's permissions list
            self.DICT['result'][user if user else group]['app_label']\
                [app_label]['content_type'][model.__name__.lower()]\
                [self._get_object_index(
                    app_label=app_label,
                    model=model,
                    object=object,
                    item=self._get_item()
                )]['permissions'].append(permission)
            return True
            
        else:
            # get object dict's permissions list
            self.DICT['result'][user if user else group]['app_label']\
                [app_label]['content_type'][model.__name__.lower()]\
                [self._get_object_index(
                    app_label=app_label,
                    model=model,
                    object=object,
                    item=self._get_item()
                )]['permissions'].append(permission)
            return True

    def set_object_level_permissions(
        self,
        model : object,
        obj : object,
        user : object | None = None,
        group : Group | None = None,
        permission_level : int = 1,
        ) -> None:
        '''
            set object level permission to user or group
            user:  instance of user model or None
            group: instance of group model or None
            permission_level;
                1: view
                2: view, add
                3: view, add, change
                4: view, add, change, delete
            model: model instance of model
            you should provide at least an user or a group
            you do not have to add model level permission to user or group
        '''
        # check user and group
        if user is None and group is None:
            raise Exception('You should provide at least user or group')
        elif user is not None and group is not None:
            raise Exception('You should provide only user or group')
        elif user is not None and group is None:
            user_or_group = user
        elif user is None and group is not None:
            user_or_group = group
        
        # get content type of model
        try:
            content_type = ContentType.objects.get_for_model(model)
        except ContentType.DoesNotExist:
            raise Exception('Model does not exist')


        # get permissions according to permission level
        permissions = self.get_permissions(permission_level, content_type)
        
        # assign permissions to user or group
        if isinstance(user_or_group, Group):
            user_or_group.permissions.set(permissions)
        else:
            user_or_group.user_permissions.set(permissions)

        # assign permissions to object
        try:
            for permission in permissions:
                assign_perm(
                    perm=permission,
                    user_or_group=user_or_group, 
                    obj=obj)
        except Exception as e:
            raise Exception(e)
        

class UserObjectLevelPermission(BaseObjectLevelPermission):
    '''
    User object level permission class
    '''
    def _is_user_exist(
            self, 
            user: str|int|object
        ) -> int:
        '''
        Check user is exist in database
        if exist return user_id
        '''
        if isinstance(user, str):
            try:
                user_id = get_user_model().objects.get(username=user).id
                return user_id
            except get_user_model().DoesNotExist as e:
                raise f"Error: {e}"
        elif isinstance(user, int):
            try:
                user_id = get_user_model().objects.get(id=user).id
                return user_id
            except get_user_model().DoesNotExist as e:
                raise f"Error: {e}"
        elif isinstance(user, object):
            user_id = user.id
            return user_id

    def _user_control(
            self, 
            user: str
        ) -> bool:
        '''
        Check user is exist in result dict
        If not exist, create new user, app_label and return True
        '''
        if user not in self.DICT['result']:
            self.DICT['result'][user] = {"app_label": {}}
        return True

    def _create_user_olp_report(
            self, 
            permissions: list, 
            content: object
        ) -> None:
        '''
        Create user permission and add to result dict
        Show all user object level permissions to each model object
        '''
        for perm in permissions:
            user = perm.user.username
            has_user = self._user_control(user)
            if has_user:
                app_label = content.app_label
                # check app label is exist in result dict
                self._app_label_control(
                    app_label=app_label,
                    user=user
                )
                # check model is exist in result dict
                model = apps.get_model(content.app_label, content.model)
                object = model.objects.get(id=perm.object_pk)
                self._model_and_object_control(
                        app_label=app_label, 
                        model=model, 
                        object=object,
                        user=user
                )
                # get permission
                permission = perm.permission.name
                # add permission to result dict
                self._set_permission(
                    app_label=app_label,
                    model=model,
                    object=object,
                    permission=permission,
                    user=user
                )
    def bulk_assign_user(
            self, 
            model : object,
            user : list, 
            obj : object,
            permission_level : int
        ) -> bool:
        '''
        Bulk assign user to object
        User must be list of user id or list of user object
        '''
        if not isinstance(user, list):
            raise TypeError('User must be list of user id or list of user object')
        for u in user:
            if isinstance(u, int):
                user = get_user_model().objects.get(id=u)
            elif isinstance(u, get_user_model()):
                user = u
            else:
                raise TypeError('User must be list of user id or list of user object')
            
            try:
                self.set_object_level_permissions(
                    model=model,
                    obj=obj,
                    user=user,
                    permission_level=permission_level
                )
            except Exception as err:
                raise Exception('Error: %s') % err
        return True

    def remove_user_permission(
            self,
            model : object,
            user : object,
            obj : object,
            permission_level : int
    ) -> bool:
        '''
        Remove user from object
        '''
        try:
            for perm in self._get_permission_name(model=model, permission_level=permission_level):
                remove_perm(
                    perm=perm,
                    user=user,
                    obj=obj
                )
            return True
        except Exception as err:
            raise Exception('Error: %s') % err

    def get_all_user_permissions(self) -> dict:
        '''
        Get all user permissions
        '''
        for content in ContentType.objects.all():
            try:
                perm = UserObjectPermission.objects.filter(
                    content_type_id=content.id
                )
                if perm.count() > 0:
                    # create user permission report
                    self._create_user_olp_report(
                        permissions=perm, 
                        content=content
                    )
            except BaseException as e:
                raise f"Error: {e}"
        return self.DICT
        
    def get_single_user_permissions(
            self, 
            user: object|int|str 
        ) -> dict:
        '''
        Get specific user object level permissions
        params: 
            user: object|int|str
        '''
        for content in ContentType.objects.all():
            try:
                perm = UserObjectPermission.objects.filter(
                    content_type_id=content.id,
                    user_id=self._is_user_exist(user)
                )
                if perm.count() > 0:
                    # create user permission report
                    self._create_user_olp_report(
                        permissions=perm, 
                        content=content
                    )
            except BaseException as e:
                raise f"Error: {e}"
        return self.DICT
    

class GroupObjectLevelPermission(BaseObjectLevelPermission):
    '''
    Group object level permission class
    '''
    def _is_group_exist(
            self, 
            group: str|int|object
        ) -> int:
        '''
        Check group is exist in database
        if exist return group_id
        '''
        if isinstance(group, str):
            try:
                group_id = Group.objects.get(name=group).id
                return group_id
            except Group.DoesNotExist as e:
                raise f"Error: {e}"
        elif isinstance(group, int):
            try:
                group_id = Group.objects.get(id=group).id
                return group_id
            except Group.DoesNotExist as e:
                raise f"Error: {e}"
        elif isinstance(group, object):
            group_id = group.id
            return group_id

    def _group_control(
            self, 
            group: str
        ) -> bool:
        '''
        Check group is exist in result dict
        If not exist, create new group, app_label and return True
        '''
        if group not in self.DICT['result']:
            self.DICT['result'][group] = {"app_label": {}}
        return True

    def _create_group_olp_report(
            self, 
            permissions: list, 
            content: object
        ) -> None:
        '''
        Create group permission and add to result dict
        Show all group object level permissions to each model object
        '''
        for perm in permissions:
            group = perm.group.name
            has_group = self._group_control(group)
            if has_group:
                app_label = content.app_label
                # check app label is exist in result dict
                self._app_label_control(
                    app_label=app_label,
                    group=group
                )
                # check model is exist in result dict
                model = apps.get_model(app_label, content.model)
                object = model.objects.get(id=perm.object_pk)
                self._model_and_object_control(
                        app_label=app_label, 
                        model=model, 
                        object=object,
                        group=group
                )
                # get permission
                permission = perm.permission.name
                # add permission to result dict
                self._set_permission(
                    app_label=app_label,
                    model=model,
                    object=object,
                    permission=permission,
                    group=group
                )

        
    def bulk_assign_group(
            self,
            model : object,
            group : list,
            obj : object,
            permission_level : int
    ) -> bool:
        '''
        Bulk assign group to object
        '''
        if not isinstance(group, list):
            raise TypeError('Group must be list of group id or list of group object')
        
        for g in group:
            if isinstance(g, int):
                group = Group.objects.get(id=g)
            elif isinstance(g, Group):
                group = g
            else:
                raise TypeError('Group must be list of group id or list of group object')
            
            try:
                self.set_object_level_permissions(
                    model=model,
                    obj=obj,
                    group=group,
                    permission_level=permission_level
                )
            except Exception as err:
                raise Exception('Error: %s') % err
        return True
    
    def remove_group_permission(
            self,
            model : object,
            group : Group,
            obj : object,
            permission_level : int
    ) -> bool:
        '''
        Remove group from object
        '''
        try:
            for perm in self._get_permission_name(model=model, permission_level=permission_level):
                remove_perm(
                    perm=perm,
                    group=group,
                    obj=obj
                )
            return True
        except Exception as err:
            raise Exception('Error: %s') % err

    def get_all_group_permissions(self) -> dict:
        '''
        Get all group permissions
        '''
        for content in ContentType.objects.all():
            # try:
                perm = GroupObjectPermission.objects.filter(
                    content_type_id=content.id
                )
                if perm.count() > 0:
                    # create group permission report
                    self._create_group_olp_report(
                        permissions=perm, 
                        content=content
                    )
            # except BaseException as e:
            #     raise f"Error: {e}"
        return self.DICT
    
    def get_single_group_permissions(
            self, 
            group: object|int|str 
        ) -> dict:
        '''
        Get specific group object level permissions
        params: 
            group: object|int|str
        '''
        for content in ContentType.objects.all():
            try:
                perm = GroupObjectPermission.objects.filter(
                    content_type_id=content.id,
                    group_id=self._is_group_exist(group)
                )
                if perm.count() > 0:
                    # create group permission report
                    self._create_group_olp_report(
                        permissions=perm, 
                        content=content
                    )
            except BaseException as e:
                raise f"Error: {e}"
        return self.DICT
    

class Validators:

    @staticmethod
    def is_user_exist(user: int) -> bool:
        '''
        Check user is exist in database
        '''
        if user is None:
            return False
        
        try:
            get_user_model().objects.get(id=user)
            return True
        except get_user_model().DoesNotExist:
            return False

    @staticmethod
    def is_group_exist(group: int) -> bool:
        '''
        Check group is exist in database
        '''
        if group is None:
            return False
        
        try:
            Group.objects.get(id=group)
            return True
        except Group.DoesNotExist:
            return False

    @staticmethod
    def is_app_label_exist(app_label: str) -> bool:
        '''
        Check app_label is exist in database
        '''
        if app_label is None or app_label == '':
            return False

        try:
            apps.get_app_config(app_label)
            return True
        except LookupError:
            return False

    @staticmethod
    def is_model_exist(app_label: str, model: str) -> bool:
        '''
        Check model is exist in database
        '''
        if Validators().is_app_label_exist(app_label=app_label) == False:
            return False
        if model is None or model == '':
            return False
        
        try:
            apps.get_model(app_label, model)
            return True
        except LookupError:
            return False
        
    @staticmethod
    def is_object_exist(app_label: str, model: str, object_id: int) -> bool:
        '''
        Check object is exist in database
        '''
        if Validators().is_model_exist(app_label=app_label, model=model) == False:
            return False
        if object_id is None or object_id == '':
            return False
        
        model = apps.get_model(app_label, model)
        try:
            model.objects.get(id=object_id)
            return True
        except model.DoesNotExist:
            return False
        
    @staticmethod
    def is_permission_range(permission: str) -> bool:
        '''
        Check permission range is valid
        '''
        if permission is None or permission == '':
            return False

        if int(permission) in range(1, 5):
            return True
        else:
            return False