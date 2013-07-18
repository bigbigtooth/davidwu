#encoding=utf-8

import time
from datetime import datetime
from xml.dom import minidom

from django.utils.timezone import utc

from davidwu import utils


class WXRequest():
    def __init__(self, xml):
        if not xml:
            raise Exception(u"XML为空!!!")
        self.xml = xml
        self.doc = minidom.parseString(xml)
        self.root = self.doc.documentElement

    def get_msg_type(self):
        if self.root:
            return self.get('MsgType')

    def get(self, tag):
        tag = self.root.getElementsByTagName(tag)
        try:
            tag = tag[0]
            return tag.childNodes[0].nodeValue
        except:
            return None


class WXResponse():
    _data = {
        'ToUserName' : '',
        'FromUserName' : '',
        'CreateTime' : '',
        'MsgType' : 'text',
        'Content' : '',
        'FuncFlag' : 0
    }
    def __init__(self, data=None):
        if data:
            self._data.update(data)

    def set_to_username(self, touser):
        if touser:
            self._data.update({'ToUserName':touser})

    def set_from_username(self, fromuser):
        if fromuser:
            self._data.update({'FromUserName':fromuser})

    def set_content(self,content):
        if content:
            self._data.update({'Content':content})

    def data(self):
        self._data.update({'CreateTime': time.mktime(datetime.timetuple(datetime.now()))})
        return utils.dict2xml(self._data)


