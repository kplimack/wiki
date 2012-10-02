from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from wiki.models import *

def index(request):
    return render_to_response('templates/index.html',
                              context_instance=RequestContext(request))
