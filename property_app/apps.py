from django.apps import AppConfig
import logging


class PropertyAppConfig(AppConfig):
    name = 'property_app'

    def ready(self):
        # Warm up the sentence-transformers model at startup to avoid
        # first-request latency when handling semantic searches.
        try:
            from .services.embedding import get_model
            get_model()
        except Exception as exc:
            logging.getLogger(__name__).exception("Failed to preload embedding model: %s", exc)
