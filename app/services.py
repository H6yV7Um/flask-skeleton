#!/usr/bin/env python
# -*- coding: utf-8 -*-
from celery import Celery
from flask import Flask
from raven.contrib.flask import Sentry
from redis import Redis
from playhouse.db_url import connect
from werkzeug.contrib.fixers import ProxyFix
from requests import Session
from requests.adapters import HTTPAdapter

import settings

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config.from_object(settings)

peewee_mysql = connect(settings.MYSQL_URL)

redis = Redis.from_url(settings.REDIS_URL)

sentry = Sentry(app, dsn=settings.SENTRY_DSN)

celery = Celery(
    app.name,
    broker=settings.BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND)
celery.conf.update(app.config)

requests = Session()
adapter = HTTPAdapter(
    pool_connections=settings.REQUESTS_POOL_SIZE,
    pool_maxsize=settings.REQUESTS_POOL_SIZE)
requests.mount('http://', adapter)
requests.mount('https://', adapter)
requests.headers['X-Caller'] = settings.SERVICE_NAME
