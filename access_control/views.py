from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from access_control.models import (
    AccessRule
)

from access_control.permissions import (
    has_permission
)

from access_control.serializers import (
    AccessRuleSerializer,
    AccessRuleUpdateSerializer
)


class AccessRulesView(APIView):

    def get(
            self,
            request,
            rule_id=None
    ):

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

        if rule_id:

            try:
                rule = (
                    AccessRule.objects.get(
                        id=rule_id
                    )
                )

            except AccessRule.DoesNotExist:
                return Response(
                    {
                        'error':
                            'Rule not found'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = (
                AccessRuleSerializer(
                    rule
                )
            )

            return Response(
                serializer.data
            )

        rules = (
            AccessRule.objects.all()
        )

        serializer = (
            AccessRuleSerializer(
                rules,
                many=True
            )
        )

        return Response(
            serializer.data
        )

    def patch(
            self,
            request,
            rule_id=None
    ):

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
                'update'
        ):
            return Response(
                {
                    'error': 'Forbidden'
                },
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            rule = (
                AccessRule.objects.get(
                    id=rule_id
                )
            )

        except AccessRule.DoesNotExist:
            return Response(
                {
                    'error':
                        'Rule not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = (
            AccessRuleUpdateSerializer(
                rule,
                data=request.data,
                partial=True
            )
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )