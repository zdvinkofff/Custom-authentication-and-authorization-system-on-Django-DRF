from django.urls import path

from business.views import (
    ProductsView
)

urlpatterns = [
    path(
        'products/',
        ProductsView.as_view()
    ),
]