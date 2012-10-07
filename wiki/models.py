from django.db import models
from django.contrib.auth.models import User

class Section(models.Model):
    name = models.CharField(max_length=50)

    @classmethod
    def create(cls, new_section):
        section = cls(name=new_section)
        return section

    def __unicode__(self):
        return self.name


class Page(models.Model):
    name = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    user = models.ForeignKey(User,null=True,blank=True,default=None)
    section = models.ForeignKey('Section')
    updated_at = models.DateTimeField(auto_now = True)

    @classmethod
    def create(cls, page_name, page_section, page_user):
        page = cls(
            name = page_name,
            section = page_section,
            user = page_user
            )
        return page

    def __unicode__(self):
        return self.name
