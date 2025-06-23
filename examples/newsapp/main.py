import os, requests
from datetime import datetime
from dotenv import load_dotenv
from fastmobile import *


load_dotenv()

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
GNEWS_API_KEY = os.getenv('GNEWS_API_KEY')

DEFAULT_LOCATION = 'New York'

def get_weather(location=DEFAULT_LOCATION):
    try:
        url = f'http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}&aqi=no'
        response = requests.get(url)
        if response.status_code == 200: return response.json()
    except Exception as e:
        print(f'Error fetching weather: {e}')
    
    # Return dummy data if request fails
    return {
        'location': {'name': location},
        'current': {
            'temp_c': -400,
            'condition': {'text': 'Error loading weather', 'icon': ''},
            'humidity': 0,
            'wind_kph': 0,
            'feelslike_c': 0
        }
    }

def get_news(category='general', max_results=5):
    try:
        url = f'https://gnews.io/api/v4/top-headlines?category={category}&lang=en&country=us&max={max_results}&apikey={GNEWS_API_KEY}'
        response = requests.get(url)
        if response.status_code == 200: return response.json()['articles']
    except Exception as e:
        print(f'Error fetching news: {e}')
    
    # Return dummy data if request fails
    return [
        {
            'title': 'Error loading news',
            'description': 'Please try again later',
            'url': '#',
            'image': '',
            'publishedAt': datetime.now().isoformat(),
            'source': {'name': 'News Service'}
        }
    ]

app, rt = fast_app()

# Enhanced styles with weather card styling - more compact version
sty = Styles(
    Style('base', fontSize=18, padding=16, backgroundColor='#f5f7fa' ),
    Style('screen-title', fontSize=22, fontWeight='bold', color='#333', marginBottom=12, textAlign='center' ),
    # Weather card styles
    Style('weather-card', backgroundColor='white', borderRadius=12, padding=14, marginBottom=16, shadowColor='#000', shadowOffset={'width': 0, 'height': 2}, shadowOpacity=0.1, shadowRadius=3, elevation=2 ),
    Style('location-row', flexDirection='row', justifyContent='space-between', alignItems='center', marginBottom=6 ),
    Style('location', fontSize=18, fontWeight='bold', color='#333' ),
    Style('date', fontSize=12, color='#888' ),
    Style('temp-condition-row', flexDirection='row', justifyContent='space-between', alignItems='center', marginBottom=10 ),
    Style('temp-main', fontSize=32, fontWeight='bold', color='#1e88e5' ),
    Style('condition-text', fontSize=16, color='#555', flex=1, textAlign='right' ),
    Style('temp-feels', fontSize=14, color='#666' ),
    Style('details-row', flexDirection='row', justifyContent='space-around', borderTopWidth=1, borderTopColor='#f0f0f0', paddingTop=10, marginTop=5 ),
    Style('detail-item', alignItems='center', flex=1 ),
    Style('detail-value', fontSize=16, fontWeight='bold', color='#333', marginBottom=2 ),
    Style('detail-label', fontSize=12, color='#888' ),
    # Location search styles
    Style('search-box', backgroundColor='white', borderRadius=10, padding=10, marginTop=10, marginBottom=16, flexDirection='row', alignItems='center', borderColor='#ddd', borderWidth=1 ),
    Style('search-input', flex=1, fontSize=16, padding=5 ),
    Style('search-button', backgroundColor='#1e88e5', borderRadius=8, padding=10, marginLeft=10 ),
    Style('search-button-text', color='white', fontWeight='bold' ),
    # News section styles
    Style('section-title', fontSize=18, fontWeight='bold', marginTop=10, marginBottom=12, color='#333' ),
    Style('news-card', backgroundColor='white', borderRadius=10, marginBottom=12, shadowColor='#000', shadowOffset={'width': 0, 'height': 1}, shadowOpacity=0.1, shadowRadius=2, elevation=1, overflow='hidden' ),
    Style('news-image-container', height=120, backgroundColor='#f0f0f0' ),
    Style('news-image', width='100%', height='100%' ),
    Style('news-content', padding=12 ),
    Style('news-source', fontSize=12, color='#888', margin='b4' ),
    Style('news-title', fontSize=16, fontWeight='bold', color='#333', marginBottom=6 ),
    Style('news-description', fontSize=14, color='#666', lineHeight=20 ),
    Style('news-date', fontSize=12, color='#888', marginTop=8, textAlign='right' ),
    # Article detail screen styles
    Style('article-container', flex=1, backgroundColor='white', padding=16 ),
    Style('article-header', marginBottom=16 ),
    Style('article-title', fontSize=22, fontWeight='bold', color='#333', margin='t4 l6 b8' ),
    Style('article-source', fontSize=12, color='#888', margin='l6 b4'),
    Style('article-source-date', flexDirection='row', justifyContent='space-between', marginBottom=16 ),
    Style('article-image', width='100%', height='100%', ),
    Style('article-image-container', height=320, backgroundColor='#f0f0f0' ),
    Style('article-content', fontSize=16, lineHeight=24, color='#333' ),
    Style('back-btn', padding=10, margin='t16 b8 l2 r4' ),
    Style('back', flex=1, padding=15, width=24, height=24 )
)

def WeatherCard(weather_data):
    location_data = weather_data['location']
    current = weather_data['current']
    return View(id='weather-container', style='weather-card')(
        # Location and date row
        View(style='location-row')(
            Text(location_data['name'], style='location'),
            Text(datetime.now().strftime('%d %b %Y'), style='date')),
        # Combined temperature and condition row to save vertical space
        View(style='temp-condition-row')(
            View(
                Text(f'{int(current['temp_c'])}°C', style='temp-main'),
                Text(f'Feels like {int(current['feelslike_c'])}°C', style='temp-feels')),
            Text(current['condition']['text'], style='condition-text'),
        ),
        # Weather details row
        View(style='details-row')(
            # Humidity detail
            View(style='detail-item')(
                Text(f'{current['humidity']}%', style='detail-value'),
                Text('Humidity', style='detail-label')),
            # Wind detail
            View(style='detail-item')(
                Text(f'{current['wind_kph']} km/h', style='detail-value'),
                Text('Wind', style='detail-label'))))

def NewsCard(article):
    return View(style='news-card', href=f'/article/{article['title']}')(
        View(style='news-image-container')(
            Img(source='images/serveimage.jpeg', style='news-image')),
        View(style='news-content')(
            Text(article['source']['name'], style='news-source'),
            Text(article['title'], numberOfLines=2, style='news-title'),
            Text(article['description'], numberOfLines=3, style='news-description')))

@rt('/')
def get(): return Doc(StackNav(NavRoute(href='tab-1', id='tab-1')))

@rt('/tab-1')
def get():
    return sty, Screen(
        Body(
            View(style='base', scroll='true')(
                # Weather section
                Text('Your Weather', style='screen-title'),
                WeatherCard(get_weather()),
                # Search box for other locations
                Form(style='search-box')(
                    TextField(placeholder='Enter city name...', style='search-input', name='location'),
                    View(style='search-button')(
                        Text('Search', style='search-button-text'),
                        Behavior(trigger='press', href='/search-weather', action='replace', target='weather-container'))),
                # News section
                Text('Latest News', style='section-title'),
                # Add news cards
                *(NewsCard(o) for o in get_news()))))

@rt('/search-weather')
def get(location:str=DEFAULT_LOCATION): return WeatherCard(get_weather(location))

@rt('/article/{title}')
def get(title: str):
    "Display a news article in detail"
    news_articles = get_news()
    article = next((a for a in news_articles if a['title']==title), None)
    # If article not found, use placeholder data
    if not article:
        article = {
            'title': title,
            'description': 'Article content not found',
            'source': {'name': 'Unknown Source'},
            'content': 'Lorem Ipsum',
            'publishedAt': datetime.now().isoformat(),
            'url': '#'
        } 
    return sty, Screen(
        Body(
            View(
                # Back button
                View(
                    Img(source='icons/back.svg', style='back'), href='/tab-1', action='back', style='back-btn'),
                # Article content
                View(
                    # Article header
                    View(style='article-image-container')(
                        View(style='article-header')(
                            Text(article['title'], style='article-title'),
                            Text(article['source']['name'], style='article-source')),
                        # Article image
                        Img(source='/images/serveimage.jpeg', style='article-image')
                    ),
                    # Read full article button (if URL available)
                    View(
                        Text(article['content'], style='base'))))))

serve(port=8085)