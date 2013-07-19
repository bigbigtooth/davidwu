#encoding=utf-8

import logging
from datetime import datetime, time
from xml.dom import minidom

import xmltodict
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from davidwu import utils
from wx import WXRequest,WXResponse

log = logging.getLogger('django')


def render(request, template, context):
    return render_to_response(template, context,
                              context_instance=RequestContext(request))


def index(request):
    return render(request, 'website/index.html', {})


@csrf_exempt
def wx(request):
    def do_command(req):
        log.debug("=========%s" % req.xml)



        resp = WXResponse()
        resp.set_from_username(req.get('ToUserName'))
        resp.set_to_username(req.get('FromUserName'))
        resp.set_content(u'你好啊')
        return resp

    if request.method == 'POST':
        xml = request.body
        if xml and xml.startswith('<xml>'):
            log.debug("=====WX Request====%s" % xml)
            resp = WXRequest(request).do()
            return HttpResponse(resp.data())

    if request.method == 'GET':
        return HttpResponse(request.GET.get('echostr'))

    return HttpResponse('')
