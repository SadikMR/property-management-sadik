from django.contrib import admin
from .models import Location, Property, PropertyImage

admin.site.register(Location)
admin.site.register(Property)
admin.site.register(PropertyImage)