"""
Settings for Django Rest Object Permission library.
This configuration is designed like DRF's settings.py file.

Author: Ali Yıldırım <ali.yildirim@tarsierteknoloji.com>
"""
from django.conf import settings
from django.core.signals import setting_changed


DEFAULTS = {
    # Default configuration settings
    'BYPASS_STAFF_USER': False,  # Give permission on all objects to staff users
    'BYPASS_GROUP_LIST': [],     # If you want to bypass permissions for specific group(s), add a list of group names.
    'BYPASS_USER_LIST': [],      # Similar to group, add a list of usernames.
}


class APISettings:
    """
    Provides user configuration options.
    """
    def __init__(self, user_settings=None, defaults=None):
        self.user_settings = user_settings or {}
        self.defaults = defaults or DEFAULTS

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError(f"Invalid setting: '{attr}'")
        return self.user_settings.get(attr, self.defaults[attr])

    def reload(self):
        self.user_settings = getattr(settings, 'DRO_CONF', {})

    @property
    def all_settings(self):
        return {**self.defaults, **self.user_settings}


api_settings = APISettings(None, DEFAULTS)


def reload_api_settings(*args, **kwargs):
    setting = kwargs['setting']
    if setting == 'DRO_CONF':
        api_settings.reload()


setting_changed.connect(reload_api_settings)

