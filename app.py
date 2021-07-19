from flask import Flask,render_template
from celery import shared_task
from celery.utils.log import get_task_logger

import threading
import json

app = Flask(__name__)

logger = get_task_logger(__name__)

results = []


class myThread(threading.Thread):
    def __init__(self, ind, lock):
        threading.Thread.__init__(self)
        self.ind = ind
        self.lock = lock

    def run(self):
        global results
        with open('data_{0}.json'.format(self.ind)) as data_file:
            data = json.load(data_file)

        with self.lock:
            results.extend(data.get(str(self.ind)))


@shared_task(bind=True)
def task():
    global results
    logger.info("Start task")
    l = threading.Lock()
    threads = [myThread(x, l) for x in range(1, 4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    res = sorted(results, key=lambda k: k['id'])
    return res



@app.route('/')
def hello_world():
    task.delay()
    return render_template("test.html")

if __name__ == '__main__':
    app.run()
