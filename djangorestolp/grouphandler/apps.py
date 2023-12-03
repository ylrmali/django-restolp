from django.apps import AppConfig

class GrouphandlerConfig(AppConfig):
    name = 'djangorestolp.grouphandler'
    verbose_name = 'Django Rest OLP Group handler'

    def ready(self):
        pass