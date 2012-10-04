from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import *
from django.contrib.auth import login, authenticate
from wiki.models import *

def index(request):
    if not request.user.is_authenticated():
        return render_to_response('templates/login.html', 
                                  context_instance=RequestContext(request))
    else:            
        u = request.user
        nav_menu_left = getSections()
        breadcrumbs = ["Home"]
        return render_to_response('templates/index.html', {
                'nav_left_menu': nav_menu_left,
                'nav_left_active': 'home',
                'breadcrumbs': breadcrumbs,
                'user': u,
                }, context_instance=RequestContext(request))

def login_user(request):
    msg = "Please login below..."
    username = password = ''
    success = False
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                success=True
            else:
                msg = "Account not found"
        else:
            msg = "Incorrect username/password"
        if success:
            return index(request)
    else:
        return render_to_response('templates/login.html', {
                'state': msg,
                'username': username,
                }, context_instance=RequestContext(request))

def getSections():
    query = Section.objects.order_by('name')
    return query
