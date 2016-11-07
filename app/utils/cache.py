# coding:utf-8
import cPickle
import time
import urlparse
from functools import wraps

from flask import request
from redis.exceptions import ConnectionError

import settings
import utils
from services import redis


def cached(expire=settings.CACHED_EXPIRE_SECONDS, tag='', namespace='views'):
    def cached_deco(func):
        @wraps(func)
        def wrapper(*func_args, **func_kwargs):
            if not settings.CACHED_CALL:
                return func(*func_args, **func_kwargs)
            try:
                redis.info()
            except ConnectionError:
                utils.log.warning("redis connection fail, can't use the cache")
                return func(*func_args, **func_kwargs)

            if namespace == 'views':
                if request.method == 'GET':
                    url = urlparse.urlsplit(request.url)
                    key = ':'.join(
                        field
                        for field in [namespace, tag, url.path, url.query]
                        if field)
                else:
                    return func(*func_args, **func_kwargs)
            elif namespace == 'funcs':
                params = '%s&%s' % (str(func_args), str(func_kwargs))
                funcname = utils.get_func_name(func)
                key = ':'.join(field
                               for field in [namespace, tag, funcname, params]
                               if field)

            data = redis.get(key)
            if data is None:
                start_time = time.time()
                result = func(*func_args, **func_kwargs)
                exec_time = (time.time() - start_time) * 1000
                if exec_time > settings.CACHED_OVER_EXEC_MILLISECONDS:
                    redis.setex(key, cPickle.dumps(result), expire)
                    utils.log.debug(u'cached:%r' % key)
                return result
            return cPickle.loads(data)

        return wrapper

    return cached_deco


def get_redislock(name,
                  timeout=settings.REDIS_LOCK_TIMEOUT,
                  blocking_timeout=None):
    ''' Useage:

    lock = get_redislock('print_arg:%s' % arg, blocking_timeout=1)
    if lock.acquire():
        try:
            do_something
        finally:
            lock.release()
    else:
        logger.warning('blocking')

    '''
    key = 'lock:' + name
    lock = redis.lock(
        name=key, timeout=timeout, blocking_timeout=blocking_timeout)
    return lock
