from unicodedata import category
from django.db import migrations
from django.core.management.base import BaseCommand
from news.models import News
from users.models import Category

class Command(BaseCommand):
    help = 'To Link existing catgories'

    def handle(self, *args, **options):
        
        for news in News.objects.filter(new_category__isnull=True):
            category = Category.objects.get(name=news.bkp_category)
            news.new_category = category
            news.save()

            
            
                


