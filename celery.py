from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

app = Celery()


# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))