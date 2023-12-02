from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group


class ObjectLevelUserSerializer(serializers.ModelSerializer):
    '''
    Object level user serializer
    '''
    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
    )
    app_label = serializers.CharField(
        max_length=255,
    )
    model_name = serializers.CharField(
        max_length=255,
    )
    object = serializers.IntegerField()
    permission_level = serializers.IntegerField(
        min_value=1,
        max_value=4,
    )

    class Meta:
        model = get_user_model()
        fields = ['user','app_label', 'model_name', 'object', 'permission_level']


class ObjectLevelGroupSerializer(serializers.ModelSerializer):
    '''
    Object level group serializer
    '''
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all()
    )
    app_label = serializers.CharField(
        max_length=255,
    )
    model_name = serializers.CharField(
        max_length=255,
    )
    object = serializers.IntegerField()
    permission_level = serializers.IntegerField(
        min_value=1,
        max_value=4,
    )

    class Meta:
        model = Group
        fields = ['group', 'app_label', 'model_name', 'object', 'permission_level']
