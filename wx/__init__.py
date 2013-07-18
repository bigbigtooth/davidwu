#encoding=utf-8

import time
import logging
from datetime import datetime
from xml.dom import minidom

from davidwu import utils

log = logging.getLogger('django')


class WXRequest():
    def __init__(self, xml):
        if not xml:
            raise Exception(u"XML为空!!!")
        self.xml = xml
        self.doc = minidom.parseString(xml)
        self.root = self.doc.documentElement

        self.resp = WXResponse()
        self.resp.set_from_username(self.get('ToUserName'))
        self.resp.set_to_username(self.get('FromUserName'))


    def get_msg_type(self):
        if self.root:
            return self.get('MsgType')

    def get(self, tag, default=None):
        try:
            tag = self.root.getElementsByTagName(tag)
            tag = tag[0]
            return tag.childNodes[0].nodeValue
        except Exception, e:
            log.error("Weixin do command Error...%s" % e)
            return default

    def do(self):
        type = self.get_msg_type()
        getattr(self, 'do_%s' % type, None)()
        return self.resp

    def do_event(self):
        if self.get('Event') == 'subscribe':
            data = {
                'PicUrl': 'http://i2.s2.dpfile.com/pc/78bb0fbbd22cfb629396e3afaf9658dc(700x700)/thumb.jpg',
                'Url': 'http://davidwu.cn',
                'Title': u'欢迎使用大牙订餐系统',
                'Description': u''
            }

            self.resp = WXResponse(type='news')
            self.resp.set_from_username(self.get('ToUserName'))
            self.resp.set_to_username(self.get('FromUserName'))

            self.resp.add_item(data)
            self.resp.add_item(data)


class WXResponse():
    _text_data = {
        'ToUserName': '',
        'FromUserName': '',
        'CreateTime': '',
        'MsgType': 'text',
        'Content': '',
        'FuncFlag': 0
    }
    _news_data = {
        'ToUserName': '',
        'FromUserName': '',
        'CreateTime': '',
        'MsgType': 'news',
        'FuncFlag': 1,
        'Articles': []
    }
    _data = _text_data

    def __init__(self, type='text'):
        self.type = type
        if type == 'text':
            self._data = self._text_data
        elif type == 'news':
            self._data = self._news_data

    def set_to_username(self, touser):
        if touser:
            self._data.update({'ToUserName': touser})

    def set_from_username(self, fromuser):
        if fromuser:
            self._data.update({'FromUserName': fromuser})

    def set_content(self, content):
        if content:
            self._data.update({'Content': content})

    def set_data(self, data):
        if data:
            self._data.update(data)

    def add_item(self, item):
        if item and type(item) == dict:
            self._data['Articles'].append({'item': item})

    def data(self):
        self._data.update({'CreateTime': time.mktime(datetime.timetuple(datetime.now()))})
        if self.type == 'news':
            self._data.update({'ArticleCount': len(self._data['Articles'])})

        return u'<xml>%s</xml>' % utils.dict2xml(self._data)


