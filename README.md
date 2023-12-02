# django-restolp

*Django model-object level permission library which is support django rest framework.*

# Installation
-------------
### 1. Install `django-restolp` library with pip.

```bash
pip install git+https://github.com/ylrmali/django-restolp.git

```

### 2. Add `django-restolp` to your `INSTALLED_APPS` setting.

```python
INSTALLED_APPS = [
    ...
    'django-restolp',
]

```

### 3. Add `AUTHENTICATION_BACKENDS` to your `settings.py` setting.

```python
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend'
)

```

### 4. Add `django-restolp.urls` to your main `urls.py` urlpatterns.

```python
    urlpatterns = [
        ...
        path('', include('django-restolp')),
        ...
    ]

```

# Usage
-------------
- You can use with url or you can import class and function in code block.

## Usage with url.
### Model Level Permissions
- **/mlp/user-perms/** -> *all user permission (GET, POST)*
- **/mlp/read-perms/** -> *requested user permission (GET)*
- **/mlp/group-perms/** -> *all group permissions (GET, POST)*

### Object Level Permissions
- **/olp/user-perms/** -> *all users object level permission (GET, POST)*
- **/olp/group-perms/** -> *all groups object level permission (GET, POST)*

## Usage in code block
### **UserModelPermission()**
```python
from django-restolp.modelpermission.utils import UserPermission
```
> methods
> 
### `get_user_permissions`
*get specific user's all permissions*
- parameters
    - user → object
- output  → dictionary

### `get_all_user_permissions`
*get all users permissions*
- parameters
    - None
- output → dictionary

### `create_group_or_assgin_user`
*create new group, assign user to group or both*
- parameters
    - group : Group | str
    - user : object | None = None
    - both : bool = False
- output → None

### `set_user_permission_api`
*set model level permission to user with API*
- parameters
    - user: int
    - permissions : list
- output → list | None

### `set_user_permission`
*set model level permission to user*
- parameters
    - user : object | str | list
    - permission_level : int
    - model : object | str
    - app_label : str
- output → None

### GroupModelLevelPermission()
```python
from django-restolp.modelpermission.utils import GroupModelLevelPermission
```

> methods
> 

### `set_group_permission`
*set model level permission to group*
- parameters
    - group : Group | str
    - permission_level : int
    - model : object | str
    - app_label : str
- output → None

### `set_group_permission_api`
*set model level permission to group with API*
- parameters
    - group : int
    - permission : list
- output → list | None

### `get_group_permissions`
*get specific group's permissions*
- parameters
    - group : Group
- output → dict

### `get_all_group_permissions`
*get all groups’ permissions*
- parameters
    - None
- output → dict

### UserObjectLevelPermission()
```python
from django-restolp.objectpermission.utils import UserObjectLevelPermission
```

> methods
>
### `get_all_user_permissions`
*get all users’ permissions*
- parameters
    - None
- output → dict

### `get_single_user_permissions`
*get specific user’s object level permissions*
- parameters
    - user: object | int | str
- output → dict

### GroupObjectLevelPermission()
```python
from django-restolp.objectpermission.utils import GroupObjectLevelPermission
```
> methods
> 
### `get_all_group_permissions`
*get all group permissions*
- parameters
    - None
- output → dict

### `get_single_group_permissions`
*get specific group object level permissions*
- parameters
    - group : object | int | str
- output → dict
