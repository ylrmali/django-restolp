# django-restolp
*Django model-object level permission library which is support django rest framework.*

## Installation
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

## Usage
* You can use with url or you can import class and function in code block.
### Usage with url.
   #### Model Level Permissions
   * **/mlp/user-perms/**  -> *all user permission (GET, POST)*
   * **/mlp/read-perms/**  -> *requested user permission (GET)*
   * **/mlp/group-perms/** -> *all group permissions (GET, POST)*
   ### Object Level Permissions
   * **/olp/user-perms/**  -> *all users object level permission (GET, POST)*
   * **/olp/group-perms/** -> *all groups object level permission (GET, POST)*

### Usage in code block
    Coming soon...
    
     
