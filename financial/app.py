from flask import Flask

app = Flask(__name__)

from api import api

app.register_blueprint(api)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)