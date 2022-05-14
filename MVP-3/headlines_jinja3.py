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


app = Flask(__name__)

RSS_FEEDS = {'toi': 'https://timesofindia.indiatimes.com/rssfeedstopstories.cms',
             'tg': 'https://tj.news/rss/topstories.xml', #telegraph uk
             }

@app.route("/")
@app.route("/<publication>")
def get_news(publication="toi"):
  feed = feedparser.parse(RSS_FEEDS[publication])
  #first_article = feed['entries'][0]
  return render_template("home.html", articles=feed['entries'])

if __name__ == "__main__":
  app.run(port=5000, debug=True)