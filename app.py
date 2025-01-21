from flask import Flask, Blueprint, jsonify
from server.file.controllers.file_controller import router as file_router

app = Flask(__name__)


def register_router(_app):
    _app.register_blueprint(file_router)


if __name__ == '__main__':
    register_router(app)
    app.run()
