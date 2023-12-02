from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


class PermissionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all()
    )

    class Meta:
        model = get_user_model()
        fields = ['user', 'user_permissions']


class GroupPermissionSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all()
    )

    class Meta:
        model = Group
        fields = ['group', 'id', 'name', 'permissions']
        read_only_fields = ['id', 'name']