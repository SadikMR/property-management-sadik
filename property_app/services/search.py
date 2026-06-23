from pgvector.django import CosineDistance

from property_app.models import Location
from property_app.services.embedding import generate_embedding


def semantic_location_search(
    query: str,
    limit: int = 5,
):
    query_embedding = generate_embedding(query)

    return (
        Location.objects
        .annotate(
            distance=CosineDistance(
                "name_embedding",
                query_embedding,
            )
        )
        .order_by("distance")[:limit]
    )