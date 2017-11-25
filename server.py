#from flask import (Flask,
#                   Response,
#                   request,
#                   send_file,
#                   render_template,
#                   jsonify)

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__, static_url_path='')
app.wsgi_app = ProxyFix(app.wsgi_app)

@app.route('/status/', methods=['GET'])
def status():
    pass

if __name__ == '__main__':
    app.debug = True
    #app.run(host=HOST, port=PORT)
    app.run()
