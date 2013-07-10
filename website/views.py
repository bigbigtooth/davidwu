#encoding=utf-8

import logging

from django.shortcuts import render_to_response
from django.template import RequestContext

log = logging.getLogger('django')



def render(request, template, context):
    return render_to_response(template, context,
                              context_instance=RequestContext(request))


def index(request):
    return render(request, 'website/index.html', {})
