import pandas as pd

from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

from property_app.models import (
    Location,
    Property,
)


class Command(BaseCommand):
    help = "Import vacation rental properties from CSV"

    def handle(self, *args, **kwargs):
        csv_file = "data/properties.csv"

        df = pd.read_csv(csv_file)

        created_locations = 0
        created_properties = 0

        for _, row in df.iterrows():

            location, location_created = Location.objects.get_or_create(
                country=row["country"],
                city=row["city"],
                name=row["location_name"],
                defaults={
                    "center": Point(
                        float(row["longitude"]),
                        float(row["latitude"]),
                    )
                },
            )

            if location_created:
                created_locations += 1

            Property.objects.create(
                location=location,
                name=row["property_name"],
                description=row["description"],
                amenities=row["amenities"],
                center=Point(
                    float(row["longitude"]),
                    float(row["latitude"]),
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