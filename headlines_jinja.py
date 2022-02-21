"""
Basic use of Jinja templates
Keep following code in home.html for this flask file
--------------------------------------------------------
<html>
    <head>
        <title>Headlines</title>
    </head>
    <body>
        <h1>Headlines</h1>
        <b>title</b><br />
        <i>published</i><br />
        <p>summary</p>
    </body>
</html>
-----------------------------------------------------------
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
  first_article = feed['entries'][0]
  return render_template("home.html")

if __name__ == "__main__":
  app.run(port=5000, debug=True)