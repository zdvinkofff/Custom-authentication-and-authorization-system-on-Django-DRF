import jwt

from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from access_control.permissions import (
    has_permission
)
from users.models import User, Session
from users.serializers import (
    RegisterSerializer,
    LoginSerializer,
    UpdateProfileSerializer
)

from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdmin

class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        password = serializer.validated_data[
            'password'
        ]

        user = User(
            first_name=serializer.validated_data[
                'first_name'
            ],
            last_name=serializer.validated_data[
                'last_name'
            ],
            middle_name=serializer.validated_data.get(
                'middle_name'
            ),
            email=serializer.validated_data[
                'email'
            ]
        )

        user.set_password(password)
        user.save()

        return Response(
            {
                'message':
                    'User registered successfully',
                'user_id': user.id
            },
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data[
            'email'
        ]

        password = serializer.validated_data[
            'password'
        ]

        try:
            user = User.objects.get(
                email=email
            )
            if not user.is_active:
                return Response(
                    {
                     "error":
                         "User is deactivated"
                    },
                    status=status.HTTP_401_UNAUTHORIZED
            )
        except User.DoesNotExist:
            return Response(
                {
                    "error":
                        "Invalid credentials"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.check_password(
            password
        ):
            return Response(
                {
                    "error":
                        "Invalid credentials"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        expires_at = timezone.now() + timedelta(days=7)

        payload = {
            "user_id": user.id,
            "exp": int(expires_at.timestamp())
        }

        token = jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm="HS256"
        )

        Session.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )

        response = Response(
            {
                "access_token": token
            }
        )

        response.set_cookie(
            key="jwt",
            value=token,
            httponly=True,
            samesite="Lax"
        )

        return response


class ProfileView(APIView):

    def patch(
            self,
            request
    ):

        if str(request.user) == 'AnonymousUser':
            return Response(
                {
                    'error':
                        'Unauthorized'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = UpdateProfileSerializer(
            data=request.data,
            partial=True,
            context={
                'user': request.user
            }
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user

        for field, value in serializer.validated_data.items():
            setattr(
                user,
                field,
                value
            )

        user.save()

        return Response(
            {
                'message':
                    'Profile updated successfully',
                'user': {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'middle_name': user.middle_name,
                    'email': user.email,
                    'role': user.role
                }
            },
            status=status.HTTP_200_OK
        )


class LogoutView(APIView):

    def post(self, request):

        token = request.COOKIES.get(
            'jwt'
        ) or request.GET.get(
            'token'
        )

        if not token:
            return Response(
                {
                    'error':
                        'Token not found'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        session = Session.objects.filter(
            token=token,
            is_active=True
        ).first()

        if session:
            session.is_active = False
            session.save()

        response = Response(
            {
                'message':
                    'Logged out successfully'
            },
            status=status.HTTP_200_OK
        )

        response.delete_cookie(
            'jwt'
        )

        return response


class AdminPanelView(APIView):

    def get(self, request):

        if str(request.user) == 'AnonymousUser':
            return Response(
                {
                    'error': 'Unauthorized'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not has_permission(
                request.user,
                'permissions',
                'read'
        ):
            return Response(
                {
                    'error': 'Forbidden'
                },
                status=status.HTTP_403_FORBIDDEN
            )

        return Response(
            {
                'message': 'Welcome admin'
            },
            status=status.HTTP_200_OK
        )

class DeleteAccountView(APIView):

    def delete(
        self,
        request
    ):

        if str(request.user) == 'AnonymousUser':
            return Response(
                {
                    'error':
                        'Unauthorized'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        request.user.is_active = False
        request.user.save()

        token = request.COOKIES.get(
            'jwt'
        )

        if token:
            session = Session.objects.filter(
                token=token,
                is_active=True
            ).first()

            if session:
                session.is_active = False
                session.save()

        response = Response(
            {
                'message':
                    'Account deleted successfully'
            },
            status=status.HTTP_200_OK
        )

        response.delete_cookie(
            'jwt'
        )

        return response