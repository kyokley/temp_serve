from flask import (Flask,
                   jsonify,
                   )
from werkzeug.contrib.fixers import ProxyFix
from sensor import Sensor

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

if __name__ == '__main__':
    app.debug = True
    #app.run(host=HOST, port=PORT)
    app.run()
