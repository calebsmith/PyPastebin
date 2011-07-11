from datetime import datetime, timedelta

BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "calebsmith"
BROKER_PASSWORD = "pbandj12"
BROKER_VHOST = "caleb-X52F"

CELERY_RESULT_BACKEND = "amqp"

CELERY_IMPORTS = ("tasks", )

CELERY_AMQP_TASK_RESULT_EXPIRES = 300

CELERYBEAT_SCHEDULE = {
    "check-for-old-entries": {
        "delete_old": "tasks.delete_old",
        "args": ()
    },
}
