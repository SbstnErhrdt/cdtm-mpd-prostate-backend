from flask import Flask, jsonify

from apis.v1 import blueprint as v1

# Init flask
app = Flask(__name__)

# Register blueprints
app.register_blueprint(v1)


@app.route("/")
def home():
    response = {
        "Hello": "world"
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
