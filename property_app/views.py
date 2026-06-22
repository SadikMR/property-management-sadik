from django.shortcuts import render
from django.db.models import Q

from .models import (
    Location,
    Property,
)

def home(request):
    return render(request, "home.html")

def property_list(request):
    query = request.GET.get(
        "location",
        ""
    )

    locations = Location.objects.filter(
        Q(name__icontains=query)
        |
        Q(city__icontains=query)
    )

    properties = Property.objects.filter(
        location__in=locations
    )

    return render(
        request,
        "property_list.html",
        {
            "properties": properties,
            "query": query,
        },
    )

def property_detail(request, slug):
    return render(
        request,
        "property_detail.html",
    )