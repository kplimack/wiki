from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import *
from django.contrib.auth import login, authenticate, logout
from wiki.models import *
import re

def index(request, section_name=None, page_name=None, page_mode=None):
    if not request.user.is_authenticated():
        return render_to_response('templates/login.html',
                                  context_instance=RequestContext(request))
    else:
        u = request.user
        sections = getSections()
        breadcrumbs = [{
            'name': "Home",
            'url': 'wiki.views.index',
            }]
        active_page_name='home'
        content_page='home'
        content_bag_extra = {}
        print "SECTION_NAME=%s" % section_name
        print "PAGE_NAME=%s" % page_name
        print "PAGE_MODE=%s" % page_mode
        if section_name is not None:
            breadcrumbs.append({
                    'name': section_name,
                    'url': 'wiki.views.index',
                    'args': section_name,
                    })
            active_page_name=section_name
            content_bag_extra = {
                'section_name': section_name,
                }
            if page_name is None:
                articles = getArticles(section_name)
                content_page='section'
                content_bag_extra['articles'] = articles
            else:
                breadcrumbs.append({
                        'name': page_name,
                        })
                page = getPage(page_name)
                if page_mode == 'edit':
                    content_page = 'page_edit'
                else:
                    content_page = 'page'
                    (page_rendered, toc) = renderPage(page.content)
                    content_bag_extra['page_rendered'] = page_rendered
                    content_bag_extra['toc'] = toc

                content_bag_extra['page_name'] = page_name
                content_bag_extra['page'] = page
        if content_page in ['home', 'section']:
            content_bag_extra['last_updated'] = getLatest()
        content_bag_common = {
            'nav_left_menu': sections,
            'nav_left_active': active_page_name,
            'breadcrumbs': breadcrumbs,
            'user': u,
            'content_page': content_page,
            'sections': sections,
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

def getPage(page_name):
    query = Page.objects.get(name=page_name)
    return query

def page_save(request, section_name, page_name):
    page = get_object_or_404(Page, name=page_name)
    try:
        page_content = request.POST['page_content_raw']
    except:
        return HttpResponseRedirect(reverse('wiki.views.index', args=(section_name, page_name)))
    else:
        page.content = page_content
        page.user = request.user
        page.save()
    return HttpResponseRedirect(reverse('wiki.views.index', args=(section_name, page_name)))

def page_rename(request, section_name, page_name):
    # though unused now, I plan to add a setion selector to the rename modal
    # since rename is essentially the same thing as move, which means I should be checking for conflicts
    page = get_object_or_404(Page, name=page_name)
    try:
        page_newname = request.POST['page_newname']
    except:
        print "RENAME FAILED. request.POST=%s" % request.POST
        return HttpResponseRedirect(reverse('wiki.views.index', args=(section_name, page_name)))
    else:
        page.name = page_newname
        page.user = request.user
        page.save()
    return HttpResponseRedirect(reverse('wiki.views.index', args=(section_name, page.name)))

def page_archive(request, section_name, page_name):
    page = get_object_or_404(Page, name=page_name)
    section_archive = get_object_or_404(Section, name='archive')
    page.section = section_archive
    page.save()
    return HttpResponseRedirect(reverse('wiki.views.index', args=(section_archive, page.name)))

def page_new(request):
    return HttpResponseRedirect(reverse('wiki.views.index'))

def section_new(request):
    return HttpResponseRedirect(reverse('wiki.views.index'))

def cleanURL(urlString):
    return "_".join(urlString.split(" "))

def getLatest(numPages=10):
    last_updated = Page.objects.order_by('-updated_at')[:numPages]
    return last_updated

def renderPage(content):
    page_rendered = ''
    leave_alone=False
    ignores_start = "<pre>"
    ignores_stop = "</pre>"
    toc = []
    for line in content.split("\n"):
        if ignores_start in line:
            leave_alone=True
        if ignores_stop in line:
            leave_alone=False
        if leave_alone:
            page_rendered += line
        else:
            page_rendered += "<br />".join(line.split("\n"))

        matchObj = re.match( r'<h[1-6]>(.*)</h[1-6]>', line, re.M|re.I)
        if matchObj:
            anchor = {
                'name': matchObj.group(1),
                'url': cleanURL(matchObj.group(1)),
                }
            toc.append(anchor)
            page_rendered += '<a name="' + anchor['url'] + '"></a>'
            print "MATCHED %s" % matchObj.group()
        else:
            print "could not match headers in: %s" % line
    return (page_rendered, toc)
