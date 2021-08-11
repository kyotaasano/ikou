from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Memo(models.Model):
    name = models.CharField(max_length=200,verbose_name='名前:')
    dsc  = models.CharField(max_length=1000,verbose_name='説明:')
    date = models.DateField(blank=True, null=True)
    pic  = models.CharField(max_length=200,verbose_name='IMG:')
       
    def __str__(self):
        return self.name

