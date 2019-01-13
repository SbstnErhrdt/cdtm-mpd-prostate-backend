import os
from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS
from apis.v1 import blueprint as v1
from apis.v1.api_admin import DbHandler as adminops
from websockets.v1.patients import PatientNamespace
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO, emit, send
import os

# Define the static directory
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')

# Init flask
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'change-this-key-later-read-from-an-env-variable'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SECRET_KEY'] = 'PROCARE-SECRET!'
socketio = SocketIO(app)

socketio.on_namespace(PatientNamespace('/patients'))


@socketio.on('message')
def handle_message(message):
    print(message["message"])
    emit('message', message)


# Init cors
cors = CORS(app)

# Register blueprints
app.register_blueprint(v1)
jwt = JWTManager(app)

# Env variables
DEBUG = os.environ.get('DEBUG', True)
ES_HOST = os.environ.get('ELASTIC_SERACH_HOST', None)
ES_USERNAME = os.environ.get('ELASTIC_SERACH_USERNAME', None)
ES_PASSWORD = os.environ.get('ELASTIC_SERACH_PASSWORD', None)

if ES_HOST is None or ES_USERNAME is None:
    print("No environment parameters set. Please specify")
    os._exit(os.EX_NOHOST)


@app.route('/', methods=['GET'])
def serve_dir_directory_index():
    return send_from_directory(static_file_dir, 'index.html')


@app.route('/<path:path>', methods=['GET'])
def serve_file_in_dir(path):
    print(path)
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        return send_from_directory(static_file_dir, 'index.html')

    return send_from_directory(static_file_dir, path)


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r

if __name__ == '__main__':

    # Create a new admin if not present
    create_admin = os.environ.get("CREATE_ADMIN", None)
    admin_password = os.environ.get("ADMIN_PASSWORD", None)
    print(create_admin)
    print(admin_password)
    if create_admin and admin_password:
        # ADMIN

        data = {
            "user_name": "admin",
            "name": "admin",
            "password": admin_password
        }
        adminops.create_default_admin(data)

        # PATIENTS

        data = {
            "user_name": "patient",
            "name": "Oliver Churchill",
            "password": admin_password,
            "age": 81,
            "stage": 3,
            "remarks": "Forgets his appointments.",
            "image_url": "/userimages/patient1.jpg",
            "phone": "0049 000000",
            "medication": [
                {
                    "name": "Sipuleucel-T",
                    "take": "2 times a day (morning, evening)",
                    "amount": "4 mg",
                },
                {
                    "name": "Zoladex (Goserelin Acetate)",
                    "take": "1 time a day (morning)",
                    "amount": "1 mg",
                }
            ],
            "doctors": [
                {
                    "name": "Dr. Peter Watt",
                    "id": "doctor"
                }
            ]
        }
        adminops.create_default_patient(data)

        data = {
            "user_name": "patient2",
            "name": "Christian Black",
            "password": admin_password,
            "age": 75,
            "stage": 1,
            "remarks": "Needs a cab home.",
            "image_url": "/userimages/patient2.jpg",
            "email": "test@cdtm.de",
            "phone": "0049 000000",
            "medication": [
                {
                    "name": "Degarelix",
                    "take": "2 times a day (morning, evening)",
                    "amount": "5 mg",
                },
                {
                    "name": "Leuprolide Acetate",
                    "take": "1 time a day (morning)",
                    "amount": "8 mg",
                }
            ],
            "doctors": [
                {
                    "name": "Dr. Peter Watt",
                    "id": "doctor"
                }
            ]
        }
        adminops.create_default_patient(data)

        data = {
            "user_name": "patient3",
            "name": "Rudolph Bean",
            "password": admin_password,
            "age": 85,
            "stage": 4,
            "remarks": "Inform son about progress.",
            "image_url": "/userimages/patient3.jpg",
            "phone": "0049 000000",
            "medication": [
                {
                    "name": "Degarelix",
                    "take": "2 times a day (morning, evening)",
                    "amount": "1 mg",
                },
                {
                    "name": "Leuprolide Acetate",
                    "take": "1 time a day (morning)",
                    "amount": "5 mg",
                }
            ],
            "doctors": [
                {
                    "name": "Dr. Peter Watt",
                    "id": "doctor"
                }
            ]
        }
        adminops.create_default_patient(data)

        data = {
            "user_name": "patient4",
            "name": "Thomas Simpson",
            "password": admin_password,
            "age": 81,
            "stage": 4,
            "remarks": "Talk with his wife about driving.",
            "image_url": "/userimages/patient4.jpg",
            "phone": "0049 000000",
            "medication": [
                {
                    "name": "Degarelix",
                    "take": "2 times a day (morning, evening)",
                    "amount": "1 mg",
                },
                {
                    "name": "Leuprolide Acetate",
                    "take": "1 time a day (morning)",
                    "amount": "7 mg",
                }
            ],
            "doctors": [
                {
                    "name": "Dr. Peter Watt",
                    "id": "doctor"
                }
            ]
        }
        adminops.create_default_patient(data)

        data = {
            "user_name": "patient5",
            "name": "Bradley Stark",
            "password": admin_password,
            "age": 51,
            "stage": 2,
            "remarks": "Inform relatives about options.",
            "image_url": "/userimages/5patient5.jpg",
            "email": "test@cdtm.de",
            "phone": "0049 000000",
            "medication": [
                {
                    "name": "Degarelix",
                    "take": "2 times a day (morning, evening)",
                    "amount": "4 mg",
                },
                {
                    "name": "Leuprolide Acetate",
                    "take": "1 time a day (morning)",
                    "amount": "4 mg",
                }
            ],
            "doctors": [
                {
                    "name": "Dr. Peter Watt",
                    "id": "doctor"
                }
            ]
        }
        adminops.create_default_patient(data)

        # DOCTORS

        data = {
            "user_name": "doctor",
            "name": "Dr. Peter Watt",
            "password": admin_password,
        }
        adminops.create_default_doctor(data)

    # Start the app
    socketio.run(app, debug=DEBUG, port=5001, host='0.0.0.0')
