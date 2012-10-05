from django.conf.urls import patterns, include, url


urlpatterns = patterns('wiki.views',
                       url(r'login/$', 'login_user', name='wiki-login'),
                       url(r'logout/$', 'logout_user', name='wiki-logout'),
                       url(r'^(?P<section_name>.*)/$', 'index', name='wiki-section'),
                       url(r'^$', 'index', name='wiki-home'),
                       url('r^(?P<page_url>).*$', 'index'),
)
