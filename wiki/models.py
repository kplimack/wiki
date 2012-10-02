from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.name

class Page(models.Model):
    name = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    author = models.ForeignKey('Author')
    
    def __unicode__(self):
        return self.name
