from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

class GroupWithUser:
    def __init__(self):
        self.groups = Group.objects.all()
        self.users = get_user_model().objects.all()

    def get_group_with_user(self) -> list:
        '''
            Return a dictionary of group with their users.
        '''
        group_with_user = []
        for group in self.groups:
            group_with_user.append({
                'id': group.id,
                'name': group.name,
                'user': [user for user in self.users if user.groups.filter(name=group.name).exists()]
            })
        return group_with_user
    
    def get_group_detail_with_user(self, group : int) -> dict:
        '''
            Return a dictionary of group with their users.
        '''
        group = self.groups.filter(id=group).first()
        result = {
            'id': group.id,
            'name': group.name,
            'user': [user for user in self.users if user.groups.filter(name=group.name).exists()]
        }
        return result

