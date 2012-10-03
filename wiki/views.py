from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from wiki.models import *

def index(request):
    nlm = getSections()
    return render_to_response('templates/index.html', {
            'nav_left_menu': nlm,
            'nav_left_active': 'home',
            }, context_instance=RequestContext(request))

def getSections():
    query = Section.objects.order_by('name')
    return query
