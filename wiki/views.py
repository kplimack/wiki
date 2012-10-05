from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import *
from django.contrib.auth import login, authenticate, logout
from wiki.models import *

def index(request, section_name=None, page_name=None):
    if not request.user.is_authenticated():
        return render_to_response('templates/login.html', 
                                  context_instance=RequestContext(request))
    else:            
        u = request.user
        nav_menu_left = getSections()
        breadcrumbs = ["Home"]
        active_page_name='home'
        content_page='home'
        content_bag_extra = {}

        if section_name != None:
            breadcrumbs.append(section_name)
            active_page_name=section_name
            articles = getArticles(section_name)
            print "ARTICLES: %s" % articles
            content_page='section'
            content_bag_extra = {
                'articles': articles,
                'section_name': section_name,
                }

        content_bag_common = { 
            'nav_left_menu': nav_menu_left,
            'nav_left_active': active_page_name,
            'breadcrumbs': breadcrumbs,
            'user': u,
            'content_page': content_page,
            }

        content_bag = dict(content_bag_common.items() + content_bag_extra.items())
        print "Content_bag=%s" % content_bag
        return render_to_response('templates/index.html', 
                                  content_bag,
                                  context_instance=RequestContext(request))

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

def logout_user(request):
    logout(request)
    return index(request)


def getSections():
    query = Section.objects.order_by('name')
    return query

def getArticles(section_name):
    query = Page.objects.filter(section__name__exact=section_name).order_by('name')
    return query
