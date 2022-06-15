from django.db import models
from users.models import Category

class News(models.Model):
    
    image =  models.ImageField(default='')
    author = models.CharField(max_length=150, blank=True, null=True)
    title = models.TextField(blank=True, null=True, unique=True)
    source = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True)
    content = models.TextField(blank=True, null=True)
    # bkp_category = models.TextField(blank=True, null=True)
    new_category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    url = models.TextField(blank=True,null=True)


    def __str__(self):
        return self.title
