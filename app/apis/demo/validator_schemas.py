#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import notify_engine

engine = notify_engine.import_engine_module('tof')

message_entry_data = {

    'caller': {
        'type': 'string',
        'empty': False,
        'maxlength': 32,
        'required': True,
    },

    'notify_engine': {
        'type': 'string',
        'empty': False,
        'maxlength': 32,
        'required': True,
        'allowed': notify_engine.get_engine_module_names()
    },

    'notify_method': {
        'type': 'string',
        'empty': False,
        'allowed': getattr(engine, 'allowed'),
        'required': True,
    },

    'send_to': {
        'type': 'list',
        'empty': False,
        'required': True,
    },

    'title': {
        'type': 'string',
        'maxlength': 128,
        'empty': False,
        'required': True,
    },

    'content': {
        'type': 'string',
        'empty': False,
        'required': True,
    },
}
