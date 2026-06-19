from django.contrib import admin
from django.utils.html import format_html

from .models import Location, Property, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 0

    readonly_fields = ("image_preview",)

    fields = (
        "image",
        "image_preview",
        "url",
        "caption",
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" />',
                obj.image.url
            )
        return "-"

    image_preview.short_description = "Preview"


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "city",
        "country",
    )

    search_fields = (
        "name",
        "city",
        "country",
    )

    list_filter = (
        "country",
        "city",
    )


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "location",
    )

    search_fields = (
        "name",
        "description",
        "location__name",
        "location__city",
    )

    list_filter = (
        "location__country",
        "location__city",
    )

    inlines = [PropertyImageInline]


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = (
        "property",
        "caption",
        "image_preview",
    )

    search_fields = (
        "caption",
        "property__name",
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" />',
                obj.image.url
            )
        return "-"

    image_preview.short_description = "Preview"