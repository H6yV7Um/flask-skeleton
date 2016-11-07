#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request
from utils.response import response
from utils.response import RetCode
from apis import validator
from . import validator_schemas
from . import handlers
from services import peewee_mysql
from models.message import Message
import settings


def entry():
    '''消息入口
    异步发送接收到的通知消息，返回task_id
    '''
    data = request.get_json()
    validator.allow_unknown = True
    if not validator.validate(data, validator_schemas.message_entry_data):
        return response(validator.errors, RetCode.PARAMS_ERROR)
    task_id = handlers.handle_message(data)
    return response({'task_id': task_id})


def notify_task(task_id):
    '''获取任务'''
    task = handlers.get_notify_task(task_id)
    result = {
        'status': task.status,
        'result': task.result,
    }
    if settings.DEBUG:
        result['traceback'] = task.traceback
    return response(result)


def records(id=None):
    with peewee_mysql:
        if request.method == 'GET' and id is None:
            order_by = request.values.get('order_by', 'id')
            order_type = request.values.get('order_type', 'desc')
            data = Message.get_record(order_by=order_by, order_type=order_type)
        elif request.method == 'GET' and id is not None:
            data = Message.get_record(id)
        elif request.method == 'POST':
            data = request.get_json()
            if not validator.validate(data,
                                      validator_schemas.message_entry_data):
                return response(validator.errors, RetCode.PARAMS_ERROR)
            data = Message.add_record(data)
        elif request.method == 'DELETE' and id is not None:
            data = Message.delete_record(id)
        elif request.method == 'PUT':
            data = request.get_json()
            if not validator.validate(data,
                                      validator_schemas.message_entry_data):
                return response(validator.errors, RetCode.PARAMS_ERROR)
            data = Message.update_record(id, data)
        return response(data)
