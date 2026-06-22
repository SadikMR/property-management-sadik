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
        "country",
    )

    search_fields = (
        "name",
        "country",
    )

    list_filter = (
        "country",
    )


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "property_type",
        "price",
        "location",
        "slug",
    )

    search_fields = (
        "title",
        "description",
        "location__name",
        "location__country",
    )

    list_filter = (
        "property_type",
        "location__country",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

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
        "property__title",
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" />',
                obj.image.url
            )
        return "-"

    image_preview.short_description = "Preview"