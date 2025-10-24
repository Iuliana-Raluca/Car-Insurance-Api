from django.apps import AppConfig
import os, sys
import logging

class CarInsuranceConfig(AppConfig):
    name = "car_insurance"

    def ready(self):
        if os.path.basename(sys.argv[0]) == "manage.py":
            skip_cmds = {"makemigrations", "migrate", "collectstatic", "shell", "dbshell", "test", "loaddata", "dumpdata"}
            if any(cmd in sys.argv for cmd in skip_cmds):
                return
        try:
            from core.scheduling import start_scheduler
            start_scheduler()
        except Exception as e:
            logging.getLogger(__name__).exception("Failed to start scheduler: %s", e)
