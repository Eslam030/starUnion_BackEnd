import threading
import time
from events.models import events  # Import your Django models here
import logging
from datetime import date
import datetime
import time

logger = logging.getLogger(__name__)


def task():
    for event in events.objects.all():
        if event.date < date.today():
            event.status = event.eventStatus.PAST
            event.save()
    print('All evnets status updated')


def background_task():
    all_done = False
    while True:
        try:
            now = datetime.datetime.now()
            if (now.hour == 0 and now.minute == 0 ):
                if now.second >= 0 and not all_done:
                    task()
                    all_done = True
            else:
                all_done = False
            time.sleep(1)
        except Exception as e:
            logger.exception(f'Error in background task: {str(e)}')


# Create a thread to run the background task
background_thread = threading.Thread(target=background_task)
# Daemonize the thread so it automatically shuts down when the main process ends
background_thread.daemon = True
background_thread.start()
