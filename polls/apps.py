from django.apps import AppConfig


class PollsConfig(AppConfig):
    """Config for poll app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
