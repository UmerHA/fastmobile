from fastmobile import *
import requests
from datetime import datetime
from pathlib import Path

# Configuration
WEATHER_API_KEY = "74b36255438c43f9b7f201327252004"
DEFAULT_LOCATION = "New York"  # Default location for weather
GNEWS_API_KEY = "22f8dc9c9fcc39942846a8c69bc30d94"

# Simple function to get weather data
def get_weather(location=DEFAULT_LOCATION):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}&aqi=no"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching weather: {e}")
    
    # Return dummy data if request fails
    return {
        "location": {"name": location},
        "current": {
            "temp_c": -400,
            "condition": {"text": "Error loading weather", "icon": ""},
            "humidity": 0,
            "wind_kph": 0,
            "feelslike_c": 0
        }
    }

# Function to get news data
def get_news(category="general", max_results=5):
    try:
        url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang=en&country=us&max={max_results}&apikey={GNEWS_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["articles"]
    except Exception as e:
        print(f"Error fetching news: {e}")
    
    # Return dummy data if request fails
    return [
        {
            "title": "Error loading news",
            "description": "Please try again later",
            "url": "#",
            "image": "",
            "publishedAt": datetime.now().isoformat(),
            "source": {"name": "News Service"}
        }
    ]

app, rt = fast_app()

# Enhanced styles with weather card styling - more compact version
sty = Styles(
    Style("base", 
        fontSize=18, 
        padding=16,
        backgroundColor="#f5f7fa"
    ),
    Style("screen-title", 
        fontSize=22, 
        fontWeight="bold", 
        color="#333",
        marginBottom=12,
        textAlign="center"
    ),
    # Weather card styles
    Style("weather-card", 
        backgroundColor="white",
        borderRadius=12,
        padding=14,
        marginBottom=16,
        shadowColor="#000",
        shadowOffset={"width": 0, "height": 2},
        shadowOpacity=0.1,
        shadowRadius=3,
        elevation=2
    ),
    Style("location-row",
        flexDirection="row", 
        justifyContent="space-between",
        alignItems="center",
        marginBottom=6
    ),
    Style("location", 
        fontSize=18, 
        fontWeight="bold",
        color="#333"
    ),
    Style("date",
        fontSize=12,
        color="#888"
    ),
    Style("temp-condition-row", 
        flexDirection="row", 
        justifyContent="space-between",
        alignItems="center",
        marginBottom=10
    ),
    Style("temp-main", 
        fontSize=32, 
        fontWeight="bold",
        color="#1e88e5"
    ),
    Style("condition-text", 
        fontSize=16, 
        color="#555",
        flex=1,
        textAlign="right"
    ),
    Style("temp-feels", 
        fontSize=14, 
        color="#666"
    ),
    Style("details-row",
        flexDirection="row",
        justifyContent="space-around",
        borderTopWidth=1,
        borderTopColor="#f0f0f0",
        paddingTop=10,
        marginTop=5
    ),
    Style("detail-item",
        alignItems="center",
        flex=1
    ),
    Style("detail-value", 
        fontSize=16, 
        fontWeight="bold",
        color="#333",
        marginBottom=2
    ),
    Style("detail-label", 
        fontSize=12, 
        color="#888"
    ),
    # Location search styles
    Style("search-box",
        backgroundColor="white",
        borderRadius=10,
        padding=10,
        marginTop=10,
        marginBottom=16,
        flexDirection="row",
        alignItems="center",
        borderColor="#ddd",
        borderWidth=1
    ),
    Style("search-input",
        flex=1,
        fontSize=16,
        padding=5
    ),
    Style("search-button",
        backgroundColor="#1e88e5",
        borderRadius=8,
        padding=10,
        marginLeft=10
    ),
    Style("search-button-text",
        color="white",
        fontWeight="bold"
    ),
    # News section styles
    Style("section-title",
        fontSize=18,
        fontWeight="bold",
        marginTop=10,
        marginBottom=12,
        color="#333"
    ),
    Style("news-card",
        backgroundColor="white",
        borderRadius=10,
        marginBottom=12,
        shadowColor="#000",
        shadowOffset={"width": 0, "height": 1},
        shadowOpacity=0.1,
        shadowRadius=2,
        elevation=1,
        overflow="hidden"
    ),
    Style("news-image-container",
        height=120,
        backgroundColor="#f0f0f0"
    ),
    Style("news-image",
        width="100%",
        height="100%"
    ),
    Style("news-content",
        padding=12
    ),
    Style("news-source",
        fontSize=12,
        color="#888",
        marginLeft=6,
        marginBottom=4
    ),
    Style("news-title",
        fontSize=16,
        fontWeight="bold",
        color="#333",
        marginBottom=6
    ),
    Style("news-description",
        fontSize=14,
        color="#666",
        lineHeight=20
    ),
    Style("news-date",
        fontSize=12,
        color="#888",
        marginTop=8,
        textAlign="right"
    ),
    # Article detail screen styles
    Style("article-container",
        flex=1,
        backgroundColor="white",
        padding=16
    ),
    Style("article-header",
        marginBottom=16
    ),
    Style("article-title",
        fontSize=22,
        fontWeight="bold",
        color="#333",
        marginTop=4,
        marginLeft=6,
        marginBottom=8
    ),
    Style("article-source-date",
        flexDirection="row",
        justifyContent="space-between",
        marginBottom=16
    ),
    Style("article-image",
        width="100%",
        height="100%",
        # backgroundColor="#f0f0f0",
        # marginBottom=16
    ),
    Style("article-image-container",
        height=320,
        backgroundColor="#f0f0f0"
    ),
    Style("article-content",
        fontSize=16,
        lineHeight=24,
        color="#333"
    ),
    Style("back-btn",
        padding=10,  # This adds 15px of padding around all sides
        marginLeft=2,
        marginRight=4,
        marginTop=16,
        marginBottom=8
    ),
    Style("back",
        flex=1,
        padding=15,  # This adds 15px of padding around all sides
        width=24,
        height=24
    )
)

def weather_card(weather_data):
    "Create a visually appealing compact weather card component"
    location_data = weather_data["location"]
    current = weather_data["current"]

    return View(style="weather-card")(
        # Location and date row
        View(style="location-row")(
            Text(location_data["name"], style="location"),
            Text(datetime.now().strftime("%d %b %Y"), style="date")
        ),
        # Combined temperature and condition row to save vertical space
        View(style="temp-condition-row")(
            View(
                Text(f"{int(current['temp_c'])}°C", style="temp-main"),
                Text(f"Feels like {int(current['feelslike_c'])}°C", style="temp-feels"),
            ),
            Text(current["condition"]["text"], style="condition-text"),
        ),
        # Weather details row
        View(style="details-row")(
            # Humidity detail
            View(style="detail-item")(
                Text(f"{current['humidity']}%", style="detail-value"),
                Text("Humidity", style="detail-label")),
            # Wind detail
            View(style="detail-item")(
                Text(f"{current['wind_kph']} km/h", style="detail-value"),
                Text("Wind", style="detail-label"))))

def news_card(article):
    """Create a news card component"""
    return View(
        # Optional image container
        View(
            # Would add image here if supported
            Img(source="images/serveimage.jpeg", style="news-image"),
            style="news-image-container"
        ),
        View(
            Text(article["source"]["name"], style="news-source"),
            Text(article["title"], numberOfLines=2, style="news-title"),
            Text(article["description"], numberOfLines=3, style="news-description"),
            # Text(format_date(article["publishedAt"]), style="news-date"),
            style="news-content"
        ),
        style="news-card",
        href=f"/article/{article["title"]}"
    )

@rt('/')
def get():
    return Doc(StackNav(NavRoute(href='tab-1', id='tab-1')))

@rt('/tab-1')
def get():
    # Get weather data for the default location
    weather_data = get_weather()
    # Get news data
    news_articles = get_news()
    return sty, Screen(
        Body(
            View(
                # Weather section
                Text('Your Weather', style="screen-title"),
                weather_card(weather_data),
                # Optional: Add a search box for other locations
                View(
                    TextField(placeholder="Enter city name...", style="search-input", id="location"),
                    View(
                        Text("Search", style="search-button-text"),
                        hx_post="/search-weather",
                        hx_target="#weather-container",
                        hx_include="[id='location']",
                        style="search-button"
                    ),
                    style="search-box"
                ),
                # Container for updated weather after search
                View(id="weather-container"),
                # News section
                Text('Latest News', style="section-title"),
                # Add news cards
                *(news_card(article) for article in news_articles),
                style="base",
                scroll="true"  # Make the content scrollable
            )
        )
    )

@rt('/')
def get():
    return Doc(StackNav(NavRoute(href='tab-1', id='tab-1')))

# Handler for searching weather by location
@rt('/search-weather')
def post(form_data):
    location = form_data.get("location", DEFAULT_LOCATION)
    weather_data = get_weather(location)
    return weather_card(weather_data)

# Article detail screen
@rt('/article/{title}')
# def get(url, title, source, date, description):
def get(title: str):
    """Display a news article in detail"""
    # formatted_date = format_date(date)
    news_articles = get_news()
    article = None
    
    for a in news_articles:
        if a["title"] == title:
            article = a
            break
    
    # If article not found, use placeholder data
    if not article:
        article = {
            "title": title,
            "description": "Article content not found",
            "source": {"name": "Unknown Source"},
            "content": "Lorem Ipsum",
            "publishedAt": datetime.now().isoformat(),
            "url": "#"
        } 
    return sty, Screen(
        Body(
            View(
                # Back button
                View(
                    View(Img(source="icons/back.svg", style="back"), href="/tab-1", action="back", style="back-btn"),
                ),
                # Article content
                View(
                    # Article header
                    View(
                        View(
                            Text(article["title"], style="article-title"),
                            Text(article["source"]["name"], style="news-source"),
                            style="article-header"
                        ),
                        # Article image
                        Img(source="/images/serveimage.jpeg", style="article-image"),
                        style='article-image-container'
                    ),
                    # Read full article button (if URL available)
                    View(
                        Text(article["content"], style="base")
                    ), 
                ),
            ),
        )
    )

serve(port=8085)