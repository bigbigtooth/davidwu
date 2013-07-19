#encoding=utf-8

import time
import logging
from datetime import datetime
from xml.dom import minidom

from django.core.cache import cache

from davidwu import utils

log = logging.getLogger('django')


class WXRequest():
    def __init__(self, request):
        self.request = request
        xml = request.body
        if not xml:
            raise Exception(u"XML为空!!!")
        self.xml = xml
        self.doc = minidom.parseString(xml)
        self.root = self.doc.documentElement

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
        return WXHandler(self).do()


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


class WXHandler():
    ''' 处理公众号业务逻辑
    '''
    check_point_key = 'u_%s_last_action'

    def __init__(self, req):
        self.req = req

        self.resp = WXResponse()
        self.resp.set_from_username(self.req.get('ToUserName'))
        self.resp.set_to_username(self.req.get('FromUserName'))

    def save_checkpoint(self, action):
        if action:
            from_user = self.req.get('FromUserName')
            cache.set(self.check_point_key % from_user, action, 600)

    def clear_checkpoint(self):
        from_user = self.req.get('FromUserName')
        return cache.delete(self.check_point_key % from_user)

    def checkpoint(self):
        from_user = self.req.get('FromUserName')
        return cache.get(self.check_point_key % from_user)

    def do(self):
        type = self.req.get_msg_type()
        getattr(self, 'do_%s' % type, None)()
        return self.resp

    def do_event(self):
        ''' 首次关注
        '''

        self.resp = WXResponse(type='news')
        self.resp.set_from_username(self.req.get('ToUserName'))
        self.resp.set_to_username(self.req.get('FromUserName'))

        if self.get('Event') == 'subscribe':
            data = {
                'PicUrl': 'http://i2.s2.dpfile.com/pc/78bb0fbbd22cfb629396e3afaf9658dc(700x700)/thumb.jpg',
                'Url': 'http://davidwu.cn',
                'Title': u'欢迎使用大牙订餐系统',
                'Description': u'输入“菜单”可以看到我们的菜单；\n 输入“我”可以查看和修改您的个人资料。'
            }

            self.resp.add_item(data)


    menus = {1: u'濑尿牛肉丸', 2 : u'黯然神伤饭', 3 : u'捞你命3000'}

    def do_text(self):
        content = self.req.get('Content')
        if content:
            is_finish = False
            print '-------Cache---------', cache._cache
            if self.checkpoint():
                print 'Yes, you start to order...'
                is_finish = getattr(self, 'doo_%s' % self.checkpoint(), None)()
                self.clear_checkpoint()

            if not is_finish:
                if content == u'菜单':
                    print '---1---'
                    menu_str = u''
                    for key, value in self.menus.iteritems():
                        menu_str += '\n [%s] : %s' % (key, value)

                    self.save_checkpoint('menu')
                    print 'Save to check point', cache._cache
                    self.resp.set_content(u'请输入下面菜单的序号订餐（可多选，用逗号隔开）：%s' % menu_str)
                elif content == u'我':
                    print '---2---'
                    pass
                else:
                    print '---3---'
                    self.resp.set_content(u'输入“菜单”可以看到我们的菜单；\n 输入“我”可以查看和修改您的个人资料。')

    def doo_menu(self):
        try:
            content = self.req.get('Content')
            if content:
                if ',' in content:
                    os = content.split(',')
                else:
                    os = [content]

                orders = {}
                for o in os:
                    if o and type(o) == int and self.menus[int(o)]:
                        if orders[int(o)]:
                            orders[int(o)] += 1
                        else:
                            orders[int(o)] = 1

                print 'Order : ', orders
                confirm_str = u''
                for key, value in orders.iteritems():
                    confirm_str += '\n%s x %s' % (key, value)
                self.resp.set_content(u'请确认订单：%s' % confirm_str)
                return True
        except Exception, e:
            log.error(e, exc_info=True)
        return False
