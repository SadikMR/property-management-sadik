from django.urls import path
from property_app.views import (
    LocationAutocompleteAPIView,
)

from . import views

urlpatterns = [
    path("", views.home, name = "home"),
    path("search/", views.property_list, name = "property_list"),
    path(
        "property/<slug:slug>/",
        views.property_detail,
        name="property_detail",
    ),
    path(
        "locations/autocomplete/",
        LocationAutocompleteAPIView.as_view(),
        name="location-autocomplete",
    ),
         
]