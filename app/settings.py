# -*- coding:utf-8 -*-
import os

from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)

JSON_AS_ASCII = config('JSON_AS_ASCII', default=False, cast=bool)
JSON_KEYCASE = config('JSON_KEYCASE', default=None)
PROJECT_ROOT_PATH = os.path.dirname(
    os.path.dirname(os.path.realpath(__file__)))

SERVICE_NAME = config('SERVICE_NAME', default='zhiyun_notifer')
API_BIND = config('API_URL', default='localhost:5000')

MYSQL_URL = config(
    'MYSQL_URL',
    default='mysql+pool://root:root@localhost:3306/test?max_connections=40&stale_timeout=300'  # noqa
)

SENTRY_DSN = config(
    'SENTRY_DSN',
    default=''  # noqa
)

LOG_LEVEL = config('LOG_LEVEL', default='info')
LOG_PATH = config("LOG_PATH", default=os.path.join(PROJECT_ROOT_PATH, 'logs'))
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)
LOG_FUNC_CALL = config('LOG_FUNC_CALL', default=True, cast=bool)
LOG_PEEWEE_SQL = config('LOG_PEEWEE_SQL', default=False, cast=bool)

REDIS_URL = config(
    'REDIS_URL', default='redis://:password@localhost:6379/0')
CACHED_CALL = config('CACHED_CALL', default=True, cast=bool)
CACHED_OVER_EXEC_MILLISECONDS = config(
    'CACHED_OVER_EXEC_MILLISECONDS', default=800, cast=int)
CACHED_EXPIRE_SECONDS = config('CACHED_EXPIRE_SECONDS', default=60, cast=int)
REDIS_LOCK_TIMEOUT = config('REDIS_LOCK_TIMEOUT', default=1800, cast=int)

EXCEPTION_RETRY_COUNT = config('EXCEPTION_RETRY_COUNT', default=2, cast=int)

# ./rabbitmqctl add_user username password
# ./rabbitmqctl set_user_tags username administrator
# ./rabbitmqctl add_vhost vhostname
# ./rabbitmqctl set_permissions -p vhostname username ".*" ".*" ".*"
BROKER_URL = config(
    'BROKER_URL',
    default='amqp://username:password@localhost:5672/vhostname'  # noqa
)
CELERY_RESULT_BACKEND = config(
    'CELERY_RESULT_BACKEND',
    default='redis://:password@localhost:6379/0'
)
CELERY_RESULT_PERSISTENT = config(
    'CELERY_RESULT_PERSISTENT', default=True, cast=bool)
FAKE_HANDLE_TASK = config('FAKE_HANDLE_TASK', default=False, cast=bool)

REQUESTS_POOL_SIZE = config('REQUESTS_POOL_SIZE', default=10, cast=int)
