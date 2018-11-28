# app.py
import time
from flask import Flask, send_from_directory, jsonify
from flask_socketio import SocketIO

from mvg import get_hauptbahnhof
from instagram import get_photos
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)

socketio = SocketIO(app)


@app.route('/')
def root():
    return app.send_static_file('./static/index.html')


@app.route("/mvg")
def rest_get_mvg():
    response = dict()
    response["mvg"] = get_hauptbahnhof()
    # return response
    return jsonify(response)


@app.route("/instagram")
def rest_get_instagram():
    return get_photos()


@app.route("/welcome")
def rest_post_welcome():
    socket_welcome_emit("Sebastian")
    return ('', 204)


def socket_welcome_emit(name):
    response = dict()
    response['message'] = "Welcome " + name
    socketio.emit('welcome', response, json=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)
    # app.run(debug=True)
