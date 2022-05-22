"""
1. Advanced use of Jinja templates
2. Passing dynamic data to template and displaying dyanamic data in the template
3. Using Jinja objects
Keep following code in home.html for this flask file
--------------------------------------------------------
<!DOCTYPE html>
<html lang="en">
    <head>
        <title><i>Headlines</title></i>
    </head>
    <body>
    <h1>Headlines</h1>
        {% for article in articles %}
            <b><a href="{{article.link}}">{{article.title}}</a></b><br />
            <i>{{article.published}}</i><br />
            <p>{{article.summary}}</p>
            <hr />
        {% endfor %}

    </body>
</html>
------------------------------------------------------------------

"""
import feedparser
from flask import Flask
from flask import render_template # for jinja html template
from flask import request # Request context from flask
import json
import urllib.request as urllib2
import urllib




app = Flask(__name__)

RSS_FEEDS = {'toi': 'https://timesofindia.indiatimes.com/rssfeedstopstories.cms',
             'tg': 'https://tj.news/rss/topstories.xml', #telegraph uk
             }
DEFAULTS = {"publication" : "toi",
            "city" : "London,UK",
            'currency_from': 'GBP',
            'currency_to': 'USD'
            }

"""
AP-key for weather data: 33b0944bf55eaae478bcbe31a56ff8f2
AP-key for currency data: 49faa00764b540ce94f09631387110bb
"""
WEATHER_URL= r"http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=33b0944bf55eaae478bcbe31a56ff8f2"
CURRENCY_URL = r"https://openexchangerates.org//api/latest.json?app_id=49faa00764b540ce94f09631387110bb"
"""
A new function get_weather(), which makes use of weather API from
https://home.openweathermap.org/
The API-key was extracted by registering to the website.
"""
def get_weather(query):
    #api_url = http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=<API-key>

    #query = urllib.quote(query) # to handle spaces for cityies variable in the query
    query = urllib.parse.quote(query)  # to handle spaces for cityies variable in the query
    url = WEATHER_URL.format(query)
    #data = urllib2.urlopen(url).read()
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description":parsed["weather"][0]["description"],
                   "temperature":parsed["main"]["temp"],
                   "city":parsed["name"],
                   'country': parsed['sys']['country']}
    return weather

def get_rates(frm, to):
    all_currency = urllib2.urlopen(CURRENCY_URL).read()
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return to_rate/frm_rate
def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


@app.route("/")
def home():
  # get customized headlines, based on user input or default
  publication = request.args.get('publication')
  if not publication:
    publication = DEFAULTS['publication']
  articles = get_news(publication)

  # get customized weather based on user input or default
  city= request.args.get("city")
  if not city:
      city = DEFAULTS['city']
  weather = get_weather(city)

  # get customized currency based on user input or default
  currency_from = request.args.get("currency_from")
  if not currency_from:
      currency_from = DEFAULTS['currency_from']
  currency_to = request.args.get("currency_to")
  if not currency_to:
      currency_to = DEFAULTS['currency_to']
  rate = get_rates(currency_from, currency_to)
  return render_template("home4.html", articles=articles, weather= weather,
                         currency_from=currency_from, currency_to=currency_to, rate=rate)
#
# @app.route("/")
# def home():
#     # get customized headlines, based on user input or default
#     publication = request.args.get('publication')
#     if not publication:
#         publication = DEFAULTS['publication']
#     articles = get_news(publication)
#     # get customized weather based on user input or default
#     city = request.args.get('city')
#     if not city:
#         city = DEFAULTS['city']
#     weather = get_weather(city)
#     return render_template("home4.html", articles=articles,weather=weather)
#
# def get_news(query):
#     if not query or query.lower() not in RSS_FEEDS:
#         publication = DEFAULTS["publication"]
#     else:
#         publication = query.lower()
#     feed = feedparser.parse(RSS_FEEDS[publication])
#     return feed['entries']
#
# def get_weather(query):
#     query = urllib.parse.quote(query)
#     url = WEATHER_URL.format(query)
#     data = urllib2.urlopen(url).read()
#     parsed = json.loads(data)
#     weather = None
#     if parsed.get('weather'):
#         weather = {'description':parsed['weather'][0]['description'],'temperature':parsed['main']['temp'],'city':parsed['name']}
#     return weather
if __name__ == "__main__":
  app.run(port=5000, debug=True)