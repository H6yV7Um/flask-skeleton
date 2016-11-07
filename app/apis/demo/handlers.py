#!/usr/bin/env python
# -*- coding: utf-8 -*-
from services import celery
from utils import log
from . import notify_engine
import settings


def handle_message(data):
    '''处理消息'''
    if settings.FAKE_HANDLE_TASK:
        log.info('received message:%r' % data)
        return 'this-is-a-fake-task-id'
    queue = data['notify_method']
    task = notify.apply_async(args=[data], queue=queue)
    return task.id


@celery.task(bind=True)
def notify(self, data):
    '''根据参数动态发送通知'''
    engine = notify_engine.import_engine_module(data['notify_engine'])
    notify_method = getattr(engine, data['notify_method'])
    result = notify_method(data['send_to'], data['title'], data['content'])
    log.debug('%r:notify complete:%r' % (self.request.id, result))
    return result


def get_notify_task(task_id):
    '''获取异步任务'''
    return notify.AsyncResult(task_id)
