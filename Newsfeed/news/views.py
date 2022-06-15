import requests
from datetime import datetime, timedelta
from django.conf import settings
from django.shortcuts import render
from users.models import Category, Profile
from news.models import News
from django.core.mail import send_mail

def upload_news():
    categories = Category.objects.all().values_list("name", flat=True)
    for category in categories:
        url = f'https://newsapi.org/v2/top-headlines?country=in&category=' + category + '&apiKey=b70f93107d924de5b1d4a1de18721507'
        response = requests.get(url).json()
        data = response["articles"]
        for i in data:
            try:
                category_instance = Category.objects.filter(name=category).first()
                News.objects.get_or_create(
                    image=i.get("urlToImage"),
                    author=i.get("author", "Dhruvi"),
                    title=i.get("title"),
                    source=i.get("source").get("name", "Internet") if i.get("source") else "Google",
                    description=i.get("description"),
                    date=i.get("publishedAt", datetime.now()),
                    content=i.get("content"),
                    url=i.get("url"),
                    new_category= category_instance,
                )
            except:
                continue
                

def mailmethod():
   
    users = Profile.objects.values('user__username','user__email','category')
    # thetime = datetime.now(tz = pytz.timezone('UTC')) - timedelta(hours=1)
    thetime = datetime.now() - timedelta(hours=1)
    for particular_user in users:
        user_news = []
        email = particular_user.get('user__email')
        
        for particular_user_category in particular_user.get('category'):
            cat_id = Category.objects.get(name=particular_user_category).id
            category_news = News.objects.filter(date__gte=thetime, new_category=cat_id).values('title', 'image', 'description', 'url', 'new_category')
            for news in category_news:
                user_news.append(news)

        subject = "New news appear here...!"
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject, str(user_news), email_from, [email], fail_silently=False)


def bind_news_from_database(list_of_category):
    news = []
    for particular_category in list_of_category:
        category_wise_data = News.objects.filter(new_category__name=particular_category)
        for particular_data in category_wise_data:
            data_bind = {'urlToImage': str(particular_data.image), 'author': particular_data.author, 'title': particular_data.title, 'source': particular_data.source, 'description': particular_data.description,
                        'publishedAt': particular_data.date, 'content': particular_data.content, 'category': particular_data.new_category, 'url':particular_data.url}
            news.append(data_bind)
    return news


def home(request):
    data = []
    category = request.GET.get("category")
    if category == 'all':
        categories = Category.objects.values_list("name", flat=True)
    elif category:
        categories = [category]
    else:
        if request.user.is_authenticated:
            categories = Profile.objects.filter(id = request.user.id).values_list("category", flat=True)[0]
        else:
            categories = Category.objects.values_list("name", flat=True)

    data = bind_news_from_database(categories)
    context = {
        'articles' : data
    }
    return render(request, 'news/home.html', context)       