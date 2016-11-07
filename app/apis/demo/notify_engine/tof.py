#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import sys
import time
sys.path.append('../..')  # noqa

import pyDes

import settings
from utils import log
from services import requests

URL = ''
APP_KEY = ''
SYS_ID = ''
BOUNDARY = 'top-api-multipart-formdata-boundary'
EMAIL_SENDER = ''


def _get_signature(random_num, timestamp, sys_id=SYS_ID):
    key = str(sys_id).ljust(8, '-')[:8]
    data = 'random{0}timestamp{1}'.format(random_num, timestamp)

    k = pyDes.des(key=key, mode=pyDes.CBC, IV=key, padmode=pyDes.PAD_PKCS5)
    sig = k.encrypt(data).encode('hex').upper()
    return sig


def _get_multipart_formdata(data):
    crlf = '\r\n'
    post_data = []
    for key, value in data.iteritems():
        if value is None:
            continue
        post_data.append('--' + BOUNDARY)
        post_data.append('Content-Type: text/plain; charset=utf-8')
        post_data.append('Content-Disposition: form-data; name="{0}"'
                         .format(key))
        post_data.append('')
        if isinstance(value, int):
            value = str(value)
        post_data.append(value)
    post_data.append('--' + BOUNDARY + '--')
    post_data.append('')
    body = crlf.join(post_data)
    return body.encode('utf-8')


def _get_headers():
    random_num = str(random.random())
    timestamp = str(int(time.time()))
    headers = {
        'appkey': APP_KEY,
        'random': random_num,
        'timestamp': timestamp,
        'signature': _get_signature(random_num, timestamp),
        'content-type': 'multipart/form-data; boundary={0}'.format(BOUNDARY)
    }
    return headers


def send(url, data):
    form_data = _get_multipart_formdata(data)
    resp = requests.post(url, headers=_get_headers(), data=form_data)
    if resp.ok:
        # noqa sucess json: {u'StackTrace': None, u'Data': True, u'ErrCode': 0, u'Ret': 0, u'ErrMsg': u''}
        res = resp.json()
        if res['ErrCode'] == 0:
            return 'SUCCESS', res
        else:
            return 'FAILURE', res
    else:
        res = u'tof api error:{0}'.format(resp.reason)
        log.error(res)
        return 'FAILURE', res


def send_email(to,
               title,
               content,
               cc=None,
               bcc=None,
               email_type=1,
               priority=0,
               body_format=0,
               sender=EMAIL_SENDER):
    if isinstance(to, list):
        to = ';'.join(rtxid for rtxid in to)
    if isinstance(cc, list):
        cc = ';'.join(rtxid for rtxid in cc)
    if isinstance(bcc, list):
        bcc = ';'.join(rtxid for rtxid in bcc)

    data = {
        'EmailType': email_type,  # 邮件类型，可选值0（外部邮件），1（内部邮件），2（约会邮件）
        'From': sender,  # 邮件发送人
        'To': to,  # 邮件接收人
        'CC': cc,  # 邮件抄送人
        'Bcc': bcc,  # 邮件密送人
        'Content': content,  # 邮件内容
        'Title': title,  # 邮件标题
        'Priority': priority,  # 邮件优先级，-1低优先级，0普通，1高优先级
        'BodyFormat': body_format,  # 邮件格式，0 文本、1 Html
    }
    url = URL + '/Message/SendMail'
    return send(url, data)


def send_rtx_tip(rtx_ids, title, msg, priority=0, sender='msng'):
    if isinstance(rtx_ids, list):
        rtx_ids = ';'.join(rid for rid in rtx_ids)

    data = {
        'MsgInfo': msg,
        'Title': title,
        'priority': priority,
        'Receiver': rtx_ids,
        'Sender': sender
    }
    url = URL + '/Message/SendRTX'
    return send(url, data)


def send_sms(rtx_ids, title, content):
    if isinstance(rtx_ids, list):
        rtx_ids = ';'.join(rtxid for rtxid in rtx_ids)

    data = {
        'MsgInfo': u'%s\n%s' % (title, content),
        'Priority': '0',
        'Receiver': rtx_ids,
        'Sender': 'zhiyun_notifer'
    }
    url = URL + '/Message/SendSMS'
    return send(url, data)


def send_weixin(rtx_ids, title, content):
    if isinstance(rtx_ids, list):
        rtx_ids = ';'.join(rtxid for rtxid in rtx_ids)

    data = {
        'MsgInfo': u'%s\n%s' % (title, content),
        'Priority': '0',
        'Receiver': rtx_ids,
        'Sender': settings.TOF_WEIXIN_SENDER
    }
    url = URL + '/Message/SendWeiXin'
    return send(url, data)


def send_rtx_msg(rtx_ids, title, msg):
    if isinstance(rtx_ids, list):
        rtx_ids = ';'.join(rid for rid in rtx_ids)
    url = 'http://dlp.isd.com/index.php/api/sendRTX'
    data = {'receiver': rtx_ids, 'title': title, 'msg': msg}
    resp = requests.post(url, json=data)
    if resp.ok:
        # noqa success json: {u'data': True, u'err_msg': u'ok', u'ret': 0, u'sender': None, u'time_used': 0.24013805389404}
        res = resp.json()
        if res['ret'] == 0:
            return 'SUCCESS', res
        else:
            return 'FAILURE', res
    else:
        res = 'send_rtx_msg api error:{0}'.format(resp.reason)
        log.error(res)
        return 'FAILURE', res


allowed = ['send_email', 'send_sms', 'send_rtx_tip', 'send_weixin',
           'send_rtx_msg']
