from flask import Flask, redirect

from server.admin.controllers.admin_controller import router as admin_router
from server.common.exception import register_error_handlers
from server.document.controllers.api_controller import \
    router as document_api_router
from server.document.controllers.view_controller import \
    router as document_router
from server.user.controllers.user_controller import router as user_router

app = Flask(__name__)


@app.route('/')
def old_page():
    return redirect('/user')


def register_router(_app):
    _app.register_blueprint(user_router)
    _app.register_blueprint(admin_router)
    _app.register_blueprint(document_router)
    _app.register_blueprint(document_api_router)


if __name__ == '__main__':
    register_router(app)
    register_error_handlers(app)
    app.run(debug=True, use_reloader=False)
