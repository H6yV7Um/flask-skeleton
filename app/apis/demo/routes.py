#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint

import utils
from utils import log
from utils import cache
from . import views

message_api = Blueprint('message', __name__)

decorators = [cache.cached(), log.log_func_call]
utils.register_decorators_on_module_funcs(views, decorators)

# 消息入口
message_api.route('/entry', methods=['POST'])(views.entry)
# 查询发送任务状态
message_api.route(
    '/notify_task/<task_id>', methods=['GET'])(views.notify_task)
# 数据库操作
message_api.route('/records', methods=['GET', 'POST'])(views.records)
message_api.route(
    '/records/<int:id>', methods=['GET', 'DELETE', 'PUT'])(views.records)
