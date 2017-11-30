import threading
import time
import LCD1602

from flask import (Flask,
                   jsonify,
                   )
from werkzeug.contrib.fixers import ProxyFix
from temp_serve.sensor import Sensor

app = Flask(__name__, static_url_path='')
app.wsgi_app = ProxyFix(app.wsgi_app)

sensor = Sensor()

@app.route('/status/', methods=['GET'])
@app.route('/status', methods=['GET'])
def status():
    res = {'status': sensor.is_initialized()}
    return jsonify(res)

@app.route('/', methods=['GET'])
def get_temp():
    res = {'celsius': sensor.get_celsius(),
           'fahrenheit': sensor.get_fahrenheit(),
           }
    return jsonify(res)

def run_forever(finished):
    LCD1602.init(0x27, 1)

    while True:
        LCD1602.write(0, 0, 'Temp: {:d}F'.format(sensor.get_fahrenheit()))
        LCD1602.write(0, 0, '      {:d}C'.format(sensor.get_celsius()))
        time.sleep(10)

        if finished.isSet():
            break

if __name__ == '__main__':
    finished = threading.Event()

    thread = threading.Thread(target=run_forever,
                              args=(finished,))
    thread.start()

    app.debug = True
    app.run(host='0.0,0,0')

    finished.set()
