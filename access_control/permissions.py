from access_control.models import (
    BusinessElement,
    AccessRule
)


def has_permission(
        user,
        element_code,
        action='read'
):

    if str(user) == 'AnonymousUser':
        return False

    if not user.role:
        return False

    try:
        element = BusinessElement.objects.get(
            code=element_code
        )

    except BusinessElement.DoesNotExist:
        return False

    rule = AccessRule.objects.filter(
        role=user.role,
        element=element
    ).first()

    if not rule:
        return False

    permission_field = (
        f'{action}_permission'
    )

    return getattr(
        rule,
        permission_field,
        False
    )