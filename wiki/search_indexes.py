import datetime
from thewikiproject.settings import HAYSTACK_USE_REALTIME_SEARCH
from haystack.indexes import *
from haystack.query import SearchQuerySet
from haystack import site, indexes
from wiki.models import Page, Section

BaseSearch = indexes.RealTimeSearchIndex if HAYSTACK_USE_REALTIME_SEARCH else indexes.SearchIndex


class PageIndex(BaseSearch):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    user = indexes.CharField(model_attr='user')
    content = indexes.CharField(model_attr='content')

    def get_model(self):
        return Page

    def index_queryset(self):
        print "RETURNING SOME OBJECTS"
        return Page.objects.all()

class SectionIndex(BaseSearch):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Section

    def index_queryset(self):
        return Section.objects.all()

site.register(Page, PageIndex)
site.register(Section,SectionIndex)
