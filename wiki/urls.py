from django.conf.urls import patterns, include, url


urlpatterns = patterns('wiki.views',
                       url(r'login/$', 'login_user', name='wiki-login'),
                       url(r'logout/$', 'logout_user', name='wiki-logout'),
                       url(r'^(?P<section_name>.*)/$', 'index', name='wiki-section'),
                       url(r'^section/new$', 'section_new', name="wiki-section-new"),
                       url(r'^page/new$', 'page_new', name="wiki-page-new"),
                       url(r'^(?P<section_name>\w+)/(?P<page_name>\w+)/save$', 'page_save', name='wiki-page-save'),
                       url(r'^(?P<section_name>\w+)/(?P<page_name>\w+)/rename$', 'page_rename', name='wiki-page-rename'),
                       url(r'^(?P<section_name>\w+)/(?P<page_name>\w+)/archive$', 'page_archive', name='wiki-page-archive'),
                       url(r'^(?P<section_name>\w+)/(?P<page_name>\w+)$', 'index', name='wiki-page-view'),
                       url(r'^(?P<section_name>\w+)/(?P<page_name>\w+)/(?P<page_mode>\w+)$', 'index', name='wiki-page-edit'),
                       url(r'^$', 'index', name='wiki-home'),
                       url('r^(?P<page_url>).*$', 'index'),
                       )
