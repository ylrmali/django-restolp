from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

class GroupSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=get_user_model().objects.all(),
        required=False,
        help_text='You do not have to specify any user for this field.'
    )

    class Meta:
        model = Group
        fields = ['id', 'name', 'user']

class GroupDetailSerializer(serializers.ModelSerializer):
    '''
        it does not work
    '''
    user = serializers.SerializerMethodField(
    )

    class Meta:
        model = Group
        fields = ['id','name', 'user']

    def get_user(self, obj):
        if isinstance(obj, Group):
            return [user.pk for user in get_user_model().objects.all() if user.groups.filter(name=obj.name).exists()]
        else:
            return [user.pk for user in get_user_model().objects.all() if user.groups.filter(name=obj.get('name')).exists()]
    

