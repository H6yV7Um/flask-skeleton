# !/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import g

from apis.demo.routes import message_api
from services import app, sentry
from utils.response import RetCode, response


@app.errorhandler(400)
def bad_request(error):
    return response(code=RetCode.PARAMS_ERROR)


@app.errorhandler(404)
def api_not_found(error):
    return response(code=RetCode.ENTRY_NOT_FOUND)


@app.errorhandler(500)
def server_error(error):
    data = {
        'sentry_event_id': g.sentry_event_id,
        'public_dsn': sentry.client.get_public_dsn('http'),
        'error': str(error)
    }
    return response(data, RetCode.SERVER_ERROR)


@app.route('/')
def hello_world():
    return response(data='Hello!')


app.register_blueprint(message_api, url_prefix='/demo')

if __name__ == '__main__':
    app.run()
