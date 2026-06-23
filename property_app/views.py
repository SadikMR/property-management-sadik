import re

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.gis.db.models.functions import Distance
from django.db.models import (
    F,
    Case,
    When,
    IntegerField,
)

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Property
from .serializers import LocationAutocompleteSerializer
from .services.search import semantic_location_search


def home(request):
    query = request.GET.get("location", "").strip()

    if query:
        locations = list(
            semantic_location_search(
                query=query,
                limit=10,
            )
        )

        location_order = Case(
            *[
                When(
                    location_id=location.id,
                    then=position,
                )
                for position, location in enumerate(locations)
            ],
            output_field=IntegerField(),
        )

        properties = (
            Property.objects
            .filter(location__in=locations)
            .annotate(rank=location_order)
            .order_by("rank")
            .select_related("location")
            .prefetch_related("images")
        )
    else:
        properties = (
            Property.objects
            .all()
            .order_by("-id")
            .select_related("location")
            .prefetch_related("images")
        )

    paginator = Paginator(properties, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "home.html",
        {
            "query": query,
            "page_obj": page_obj,
        },
    )


def property_list(request):
    query = request.GET.get("location", "").strip()

    if query:
        locations = list(
            semantic_location_search(
                query=query,
                limit=10,
            )
        )

        location_order = Case(
            *[
                When(
                    location_id=location.id,
                    then=position,
                )
                for position, location in enumerate(locations)
            ],
            output_field=IntegerField(),
        )

        properties = (
            Property.objects
            .filter(location__in=locations)
            .annotate(rank=location_order)
            .order_by("rank")
            .select_related("location")
            .prefetch_related("images")
        )
    else:
        properties = (
            Property.objects
            .all()
            .select_related("location")
            .prefetch_related("images")
        )

    paginator = Paginator(properties, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "property_list.html",
        {
            "query": query,
            "page_obj": page_obj,
        },
    )


def property_detail(request, slug):
    property = get_object_or_404(
        Property.objects
        .annotate(
            distance_from_location=Distance(
                "center",
                F("location__center"),
            )
        )
        .select_related("location")
        .prefetch_related("images"),
        slug=slug,
    )

    amenities_list = []

    if property.amenities:
        amenities_list = [
            amenity.strip()
            for amenity in re.split(
                r"[;,\n]",
                property.amenities,
            )
            if amenity.strip()
        ]

    return render(
        request,
        "property_detail.html",
        {
            "property": property,
            "amenities_list": amenities_list,
        },
    )


class LocationAutocompleteAPIView(APIView):

    def get(self, request):
        query = request.GET.get(
            "q",
            "",
        ).strip()

        if not query:
            return Response([])

        locations = semantic_location_search(
            query=query,
            limit=5,
        )

        serializer = LocationAutocompleteSerializer(
            locations,
            many=True,
        )

        return Response(serializer.data)