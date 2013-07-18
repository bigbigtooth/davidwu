# encoding=utf-8

import logging

log = logging.getLogger('django')

def dict2xml(obj):
    if obj:
        xml = u''
        for key,value in obj.iteritems():
            if type(value) in (str, unicode):
                xml += u'<%s><![CDATA[%s]]></%s>' % (key, value, key)
            elif type(value) == dict:
                xml += u'<%s>%s</%s>' % (key, dict2xml(value), key)
            elif type(value) in (list, tuple,):
                v_str = u''
                for v in value:
                    v_str += dict2xml(v)
                xml += u'<%s>%s</%s>' % (key, v_str, key)
            else:
                xml += u'<%s>%s</%s>' % (key, value, key)
        return xml
    return None