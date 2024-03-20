"""
Settings for Django Rest Object Permission library.
This configuration desined like DRF settings.py file.

https://www.django-rest-framework.org -> Django Rest Framework

Author: Ali Yıldırım <ali.yildirim@tarsierteknoloji.com>
"""
from django.conf import settings
from django.core.signals import setting_changed


DEFAULTS = {
    # default configuration settings
    'BYPASS_STAFF_USER': False,  # it give permission on all objects to staff user
    'BYPASS_GROUP_LIST': None,  # if you want to bypass perms for a specific group(s) just add an list of group name.
    'BYPASS_USER_LIST': None,  # like group, just add an list of username.
}


class APISettings:
    """
    Give the user choosing option.
    """
    def __init__(self, user_settings=None, defaults=None):
        if user_settings:
            self._user_settings = get_user_settings
        self.defaults = defaults or DEFAULTS

    @property
    def get_user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, 'DRO_CONF', {})
        return self._user_settings

api_settings = APISettings(None, DEFAULTS)

def reload_api_settings(*args, **kwargs):
    setting = kwargs['setting']
    if setting = 'DRO_CONF':
        api_settings.reload()

setting_changed.connect(reload_api_settings)

