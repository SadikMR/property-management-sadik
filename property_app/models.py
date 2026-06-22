from django.contrib.gis.db import models
from pgvector.django import VectorField


class Location(models.Model):
    country = models.CharField(
        max_length=100
    )

    city = models.CharField(
        max_length=100
    )

    name = models.CharField(
        max_length=255
    )

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

    title = models.CharField(
        max_length=255
    )

    slug = models.SlugField(
        unique=True,
        default=""
    )
    
    property_type = models.CharField(
        max_length=100,
        default=""
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

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
        return self.title


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="images"
    )

    caption = models.CharField(
        max_length=255,
        blank=True
    )

    image = models.ImageField(
        upload_to="property_images/",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.caption or f"Image for {self.property.title}"