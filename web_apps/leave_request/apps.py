from django.apps import AppConfig


class LeaveRequestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'leave_request'

    def ready(self) -> None:
        super().ready()
        import leave_request.signals
