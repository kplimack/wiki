from django.db import models
from django.contrib.auth.models import User

class Section(models.Model):
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.name

class Page(models.Model):
    name = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    author = models.ForeignKey(User, unique=True)
    section = models.ForeignKey('Section')
    def __unicode__(self):
        return self.name
