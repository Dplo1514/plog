from flask import Flask, redirect
from server.file.controllers.file_controller import router as file_router
from server.user.controllers.user_controller import router as user_router
from server.admin.controllers.admin_controller import router as admin_router

app = Flask(__name__)


@app.route('/')
def old_page():
    return redirect('/user')


def register_router(_app):
    _app.register_blueprint(file_router)
    _app.register_blueprint(user_router)
    _app.register_blueprint(admin_router)


if __name__ == '__main__':
    register_router(app)
    app.run()
