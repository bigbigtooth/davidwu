# encoding=utf-8

import logging

log = logging.getLogger('django')

def dict2xml(obj, start_node = 'xml'):
    if obj:
        xml = u'<%s>' % start_node
        for key,value in obj.iteritems():
            if type(value) in (str, unicode):
                xml += u'<%s><![CDATA[%s]]></%s>' % (key, value, key)
            else:
                xml += u'<%s>%s</%s>' % (key, value, key)
        xml += u'</%s>' % start_node
        return xml
    return None