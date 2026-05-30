from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):

    def has_permission(
        self,
        request,
        view
    ):
        return (
            request.user and
            str(request.user) != 'AnonymousUser' and
            request.user.role == 'admin'
        )