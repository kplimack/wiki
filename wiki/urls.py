from django.conf.urls import patterns, include, url


urlpatterns = patterns('wiki.views',
                       url(r'^$', 'index', name='wiki-home'),
                       url('r^(?P<page_url>).*$', 'index'),
)
