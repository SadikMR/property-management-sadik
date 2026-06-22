from django.core.paginator import Paginator

from django.shortcuts import (
    render,
    get_object_or_404,
)
from django.contrib.gis.db.models.functions import Distance
from django.db.models import F
from django.shortcuts import (
    render,
    get_object_or_404,
)

from .models import (
    Location,
    Property,
)


def home(request):
    query = request.GET.get("search", "")

    if query:
        locations = Location.objects.filter(
            name__icontains=query
        )
        properties = Property.objects.filter(
            location__in=locations
        )
    else:
        properties = Property.objects.all()

    paginator = Paginator(properties, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "query": query,
        "page_obj": page_obj,
    }

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render(request, "property_grid.html", context)

    return render(request, "home.html", context)


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

    paginator = Paginator(
        properties,
        9
    )

    page_number = request.GET.get(
        "page"
    )

    page_obj = paginator.get_page(
        page_number
    )

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
        Property.objects.annotate(
            distance_from_location=Distance(
                "center",
                F("location__center")
            )
        ),
        slug=slug,
    )

    return render(
        request,
        "property_detail.html",
        {
            "property": property,
        },
    )