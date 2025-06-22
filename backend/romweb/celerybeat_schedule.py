from celery.schedules import crontab


CELERYBEAT_SCHEDULE = {
    # Internal tasks
    "clearsessions": {
        "schedule": crontab(hour=3, minute=0),
        "task": "users.tasks.clearsessions",
    },
    "ping_stringutils_healthcheck": {
        "schedule": crontab(minute="*/14", hour="8-20", day_of_week="0-6"),
        "task": "tools.tasks.ping_stringutils_healthcheck",
    },
}
