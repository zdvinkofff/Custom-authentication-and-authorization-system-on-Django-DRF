from rest_framework import serializers

from access_control.models import (
    AccessRule
)


class AccessRuleSerializer(
    serializers.ModelSerializer
):

    role = serializers.StringRelatedField()
    element = serializers.StringRelatedField()

    class Meta:
        model = AccessRule

        fields = '__all__'


class AccessRuleUpdateSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = AccessRule

        fields = [
            'read_permission',
            'create_permission',
            'update_permission',
            'delete_permission'
        ]