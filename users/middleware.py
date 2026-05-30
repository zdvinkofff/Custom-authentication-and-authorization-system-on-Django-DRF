import jwt

from django.conf import settings
from django.contrib.auth.models import AnonymousUser

from users.models import (
    User,
    Session
)


class JWTAuthenticationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        token = request.COOKIES.get(
            'jwt'
        )

        if not token:
            auth_header = request.headers.get(
                'Authorization'
            )

            if (
                auth_header and
                auth_header.startswith(
                    'Bearer '
                )
            ):
                token = auth_header.split(
                    ' '
                )[1]

        if not token:
            token = request.GET.get(
                'token'
            )

        if token:
            try:
                session = Session.objects.filter(
                    token=token,
                    is_active=True
                ).first()

                if not session:
                    request.user = AnonymousUser()

                else:
                    payload = jwt.decode(
                        token,
                        settings.SECRET_KEY,
                        algorithms=['HS256']
                    )

                    user = User.objects.get(
                        id=payload['user_id']
                    )

                    request.user = user

            except Exception as e:
                print(
                    'JWT ERROR:',
                    e
                )

                request.user = AnonymousUser()

        else:
            request.user = AnonymousUser()

        response = self.get_response(
            request
        )

        return response