from django.core import management

from romweb import celery_app


@celery_app.task
def clearsessions():
    management.call_command("clearsessions")
