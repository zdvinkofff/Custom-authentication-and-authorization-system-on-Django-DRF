from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from access_control.permissions import (
    has_permission
)


class ProductsView(APIView):

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
                'products',
                'read'
        ):
            return Response(
                {
                    'error': 'Forbidden'
                },
                status=status.HTTP_403_FORBIDDEN
            )

        return Response(
            [
                {
                    'id': 1,
                    'name': 'Laptop'
                },
                {
                    'id': 2,
                    'name': 'Keyboard'
                }
            ],
            status=status.HTTP_200_OK
        )