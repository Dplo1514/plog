import json
import traceback
from http import HTTPStatus
from typing import Optional, Any

from flask import jsonify, request, current_app
from werkzeug.exceptions import HTTPException

from server.common.logger import error_logger
from server.common.response import Response
from server.common.status import BaseStatus, CommonStatus


class AppException(Exception):
    def __init__(
        self,
        http_status: HTTPStatus,
        status: BaseStatus,
        exception: Optional[Exception] = None,
        data: Any = None
    ):
        self.http_status = http_status
        self.exception = exception
        self.response = Response(
            code=status.code,
            message=status.message,
            data=data
        )


def exception_handler(logging_func, http_status: int, response: Response):
    logging_func()
    return jsonify(response.model_dump()), http_status


def http_exception_logging(exc: AppException):
    """ HTTP 예외 로깅 """
    log_data = {
        "url": request.url,
        "method": request.method,
        "exception": str(exc.exception),
        "response_info": {
            "http_status": exc.http_status.value,
            "code": exc.response.code,
            "message": exc.response.message,
            "data": exc.response.data,
        },
    }
    error_logger.error(json.dumps(log_data, indent=2))


def global_exception_logging(exc: Exception):
    error_logger.error(f"Unexpected Exception: {str(exc)}", exc_info=True)


def register_error_handlers(app):
    @app.errorhandler(AppException)
    def handle_app_exception(exc: AppException):
        return exception_handler(
            logging_func=lambda: http_exception_logging(exc),
            http_status=exc.http_status.value,
            response=exc.response
        )

    @app.errorhandler(HTTPException)
    def handle_http_exception(exc: HTTPException):
        response = Response(
            code=exc.code,
            message=exc.name,
            data={}
        )
        return exception_handler(
            logging_func=lambda: error_logger.error(f"HTTP Exception: {exc}"),
            http_status=exc.code,
            response=response
        )

    @app.errorhandler(Exception)
    def handle_global_exception(exc: Exception):
        response = Response(
            code=CommonStatus.INTERNAL_SERVER_ERROR.code,
            message=CommonStatus.INTERNAL_SERVER_ERROR.message,
            data={}
        )
        return exception_handler(
            logging_func=lambda: global_exception_logging(exc),
            http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
            response=response
        )
