import os
from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS
from apis.v1 import blueprint as v1
from  apis.v1.api_admin import DbHandler as adminops
from flask_jwt_extended import JWTManager
import os



# Define the static directory
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')

# Init flask
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'change-this-key-later-read-from-an-env-variable'
app.config['PROPAGATE_EXCEPTIONS'] = True

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


if __name__ == '__main__':

    # Create a new admin if not present
    create_admin = os.environ.get("CREATE_ADMIN", None)
    admin_password = os.environ.get("ADMIN_PASSWORD", None)
    if create_admin and admin_password:
        data = {
            "name": "default_admin",
            "password": admin_password
        }
        adminops.create_default_admin(data)

    # Start the app
    app.run(debug=DEBUG, port=5000, host='0.0.0.0')
