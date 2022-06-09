from datetime import datetime, timedelta
from email import message
from sre_parse import CATEGORIES
import django
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
import requests
from Newsfeed.settings import EMAIL_HOST_USER
from users.models import Category, Profile
from news.models import News
from django.contrib.auth.models import User
from django.core.mail import send_mail
import pytz
from pytz import utc

def uploadNews():
    categories = Category.objects.all().values_list("name", flat=True)
    for category in categories:
        url = f'https://newsapi.org/v2/top-headlines?country=in&category=' + category + '&apiKey=b70f93107d924de5b1d4a1de18721507'
        response = requests.get(url).json()
        data = response["articles"]
        for i in data:
            try:
                a = Category.objects.filter(name=category).first()
                News.objects.get_or_create(
                    
                    image=i.get("urlToImage"),
                    author=i.get("author", "Dhruvi"),
                    title=i.get("title"),
                    source=i.get("source").get("name", "Internet") if i.get("source") else "Google",
                    description=i.get("description"),
                    date=i.get("publishedAt", datetime.now()),
                    content=i.get("content"),
                    url=i.get("url"),
                    new_category= a,
                    
                )
            except:
                "Duplication occured....!"


def mailmethod():
    # mail = User.objects.get(id=2).email
    # users = User.objects.all()
    # users = User.objects.values('username','email') 
    # UserCategories = Profile.objects.values_list("category", flat=True)
    # users.append(UserCategories)

    users = Profile.objects.values('user__username','user__email','category')
    categories = Category.objects.all().values_list("name", flat=True)
    thetime = datetime.now(tz = pytz.timezone('UTC')) - timedelta(hours=1)
    for nUsers in users:
        userNews = []
        email = nUsers.get('user__email')
        
        for iCategory in nUsers.get('category'):
            cat_id = Category.objects.get(name=iCategory).id
            newsData = News.objects.filter(date__gte=thetime, new_category = cat_id).values('title', 'image', 'description', 'url', 'new_category')
            for oNews in newsData:
                # breakpoint()
                oNews["new_category"] = iCategory
                userNews.append(oNews)

        subject = "New news appear here...!"
        email_from = settings.EMAIL_HOST_USER
        # breakpoint()
        send_mail(subject, str(userNews), email_from, [email], fail_silently=False)


                # Profile_obj = Profile.objects.filter(category__contains = ["technology"])

                # for i in range(0,len(Profile_obj)):
                #     a1 = Profile_obj[i].user_id
                #     u1.append(User.objects.get(id=a1).email)
                #     print(u1)
                # us_obj = User.objects.all()
                # u1 = []
                
                # subject = "New news appear here...!"
                # message = userNews
                # email_from = settings.EMAIL_HOST_USER
                # recipient_list = u1
                # for i in range(0,len(Profile_obj)):
                #     a1 = Profile_obj[i].user_id
                #     u1.append(User.objects.get(id=a1).email)
                #     print(u1)
                # send_mail(
                #     subject, message, email_from, recipient_list,
                # )
                

def bindNews(category=None):
    categories = []
    if(category == None):
        categories = Category.objects.all().values_list("name", flat=True)
    else:
        if(type(category) == list):
            categories = category
        else:
            categories = [category]
    news = []
    for category in categories:
        cat_id = Category.objects.get(name=category).id
        categoryData = News.objects.filter(new_category=cat_id)
        for newsData in categoryData:
            tempData = {'urlToImage': str(newsData.image), 'author': newsData.author, 'title': newsData.title, 'source': newsData.source, 'description': newsData.description,
                        'publishedAt': newsData.date, 'content': newsData.content, 'category': newsData.new_category, 'url':newsData.url}
            news.append(tempData)
    return news
            


def home(request):
    # mailmethod()
    # uploadNews()  
    mydata = [] 
    # breakpoint()
    fixCategory = []
    # b = []
    # a = request.user
    # b.append(a)
    # a = User.objects.get("id")
    fixCategory = request.GET.get("category")
    # breakpoint()
    if(fixCategory == None):
        UserCategories = [] 
        # cat_id = Category.objects.get(name=category).id 
        # id = request.user.id
        UserCategories = Profile.objects.filter(id = request.user.id).values_list("category", flat=True)[0]
        # UserCategories = Profile.objects.values_list("category", flat=True)[b]
        # UserCategories = Profile.objects.all().values_list("category", flat=True)[0]
        mydata = bindNews(UserCategories)
    elif(fixCategory == 'all'):
        UserCategories = ["general", "entertainment", "science",
                          "sports", "health", "technology", "business"]
        mydata = bindNews(UserCategories)
    else:
        mydata = bindNews(fixCategory)
    context = {
        'articles': mydata
    }
    return render(request, 'news/home.html', context)
