from django.shortcuts import (
    render,
    get_object_or_404,
)

from .models import (
    Location,
    Property,
)


def home(request):
    return render(
        request,
        "home.html",
    )


def property_list(request):
    query = request.GET.get(
        "location",
        ""
    )

    locations = Location.objects.filter(
        name__icontains=query
    )

    properties = Property.objects.filter(
        location__in=locations
    )

    return render(
        request,
        "property_list.html",
        {
            "query": query,
            "properties": properties,
        },
    )


def property_detail(request, slug):
    property = get_object_or_404(
        Property,
        slug=slug
    )

    return render(
        request,
        "property_detail.html",
        {
            "property": property,
        },
    )