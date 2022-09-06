from flask import Flask, render_template
from turbo_flask import Turbo
import time
import threading
import sys
import random

app = Flask(__name__)
application = app
turbo = Turbo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/messages')
def messages():
    return render_template('messages.html')

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()

def update_load():
    with app.app_context():
        while True:
            time.sleep(5)
            turbo.push(turbo.replace(render_template('loadavg.html'), 'load'))

@app.context_processor
def inject_load():
    if sys.platform.startswith('linux'): 
        with open('/proc/loadavg', 'rt') as f:
            load = f.read().split()[0:3]
    else:
        load = [int(random.random() * 100) / 100 for _ in range(3)]
    return {'load1': load[0], 'load5': load[1], 'load15': load[2]}
