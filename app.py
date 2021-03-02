
from flask import Flask, request, jsonify, render_template, make_response
from flask_socketio import SocketIO
import json

import calculator
import pyutilib.subprocess.GlobalData
pyutilib.subprocess.GlobalData.DEFINE_SIGNAL_HANDLERS_DEFAULT = False

app = Flask(__name__)
io = SocketIO(app)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/calc', methods=['POST'])
def calc():
    if request.method == "POST":
        payload = request.json
        result = calculator.calculate(payload)

        io.emit('calculation_sent', json.dumps(result), broadcast=True)

        return make_response(jsonify(result), 200)


@io.on('connected')
def connected():
    app.logger.info("{} connected".format(request.namespace.socket.sessid))


@io.on('disconnect')
def disconnect():
    app.logger.info("{} disconnected".format(request.namespace.socket.sessid))


@io.on_error
def on_error(error):
    app.logger.error(error)


if __name__ == '__main__':
    io.init_app(app, engineio_logger=True, logger=True, cors_allowed_origins="*")
    io.run(app, port=5000, host='0.0.0.0')
