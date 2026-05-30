from rest_framework import serializers

from users.models import User


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(
        max_length=100
    )

    last_name = serializers.CharField(
        max_length=100
    )

    middle_name = serializers.CharField(
        required=False,
        allow_blank=True
    )

    email = serializers.EmailField()

    password = serializers.CharField(
        min_length=6,
        write_only=True
    )

    password_repeat = serializers.CharField(
        write_only=True
    )

    def validate_email(self, value):
        if User.objects.filter(
                email=value
        ).exists():
            raise serializers.ValidationError(
                'Email already exists'
            )

        return value

    def validate(self, attrs):
        password = attrs.get(
            'password'
        )

        password_repeat = attrs.get(
            'password_repeat'
        )

        if password != password_repeat:
            raise serializers.ValidationError(
                'Passwords do not match'
            )

        return attrs

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True
    )

class UpdateProfileSerializer(
    serializers.Serializer
):

    first_name = serializers.CharField(
        max_length=100,
        required=False
    )

    last_name = serializers.CharField(
        max_length=100,
        required=False
    )

    middle_name = serializers.CharField(
        required=False,
        allow_blank=True
    )

    email = serializers.EmailField(
        required=False
    )

    def validate_email(
        self,
        value
    ):
        user = self.context.get(
            'user'
        )

        existing_user = User.objects.filter(
            email=value
        ).exclude(
            id=user.id
        ).first()

        if existing_user:
            raise serializers.ValidationError(
                'Email already exists'
            )

        return value