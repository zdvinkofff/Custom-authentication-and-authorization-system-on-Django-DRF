from django.urls import path

from access_control.views import (
    AccessRulesView
)

urlpatterns = [
    path(
        'rules/',
        AccessRulesView.as_view()
    ),

    path(
        'rules/<int:rule_id>/',
        AccessRulesView.as_view()
    ),
]