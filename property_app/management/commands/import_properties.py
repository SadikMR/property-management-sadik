import pandas as pd

from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from django.utils.text import slugify

from property_app.models import (
    Location,
    Property,
)


class Command(BaseCommand):
    help = "Import properties from CSV"

    def handle(self, *args, **kwargs):
        csv_file = "data/properties.csv"

        df = pd.read_csv(csv_file)

        created_locations = 0
        created_properties = 0

        for _, row in df.iterrows():

            location, location_created = (
                Location.objects.get_or_create(
                    country=row["country"],
                    name=row["location_name"],
                    defaults={
                        "center": Point(
                            float(row["location_longitude"]),
                            float(row["location_latitude"]),
                            srid=4326,
                        )
                    },
                )
            )

            if location_created:
                created_locations += 1

            Property.objects.create(
                location=location,
                title=row["property_title"],
                slug=slugify(row["property_title"]),
                property_type=row["property_type"],
                price=row["price"],
                description=row["description"],
                amenities=row["amenities"],
                center=Point(
                    float(row["property_longitude"]),
                    float(row["property_latitude"]),
                    srid=4326,
                ),
            )

            created_properties += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"""
Import completed successfully

Locations created : {created_locations}
Properties created: {created_properties}
"""
            )
        )