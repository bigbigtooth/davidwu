#encoding=utf-8

import logging

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

log = logging.getLogger('django')



def render(request, template, context):
    return render_to_response(template, context,
                              context_instance=RequestContext(request))


def index(request):
    return render(request, 'website/index.html', {})


@csrf_exempt
def wx(request):
    log.debug("=======GET======%s" % request.GET)
    log.debug("=======POST======%s" % request.POST)
    return HttpResponse(request.GET.get('echostr', None))