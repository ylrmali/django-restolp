# django-restolp
Django object level permission library which is support rest api.

## Installation
```bash
pip install git+https://github.com/ylrmali/django-restolp.git
```

## Usage
### 1. Add `django-restolp` to your `INSTALLED_APPS` setting.
```python
INSTALLED_APPS = [
    ...
    'restolp',
]
```

### 2. Add `AUTHENTICATION_BACKENDS` to your `settings.py` setting.
```python
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', 
    'guardian.backends.ObjectPermissionBackend'
)
```
### 3. Add `django-restolp.urls` to your main `urls.py` urlpatterns.
```python
    urlpatterns = [
        ...
        path('', include('django-restolp')),
        ...
    ]
```
