from django.contrib.gis.db import models
from pgvector.django import VectorField


class Location(models.Model):
    country = models.CharField(max_length=100)

    city = models.CharField(max_length=100)

    name = models.CharField(max_length=255)

    name_embedding = VectorField(
        dimensions=384,  
        null=True,
        blank=True
    )

    center = models.PointField(
        geography=True,
        srid=4326
    )

    def __str__(self):
        return f"{self.name}, {self.city}"


class Property(models.Model):
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="properties"
    )

    name = models.CharField(max_length=255)

    description = models.TextField(
        blank=True
    )

    amenities = models.TextField(
        blank=True
    )

    center = models.PointField(
        geography=True,
        srid=4326
    )

    def __str__(self):
        return self.name


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="images"
    )

    url = models.URLField(
        blank=True
    )

    caption = models.CharField(
        max_length=255,
        blank=True
    )

    image = models.ImageField(
        upload_to="property_images/"
    )

    def __str__(self):
        return self.caption or f"Image {self.pk}"