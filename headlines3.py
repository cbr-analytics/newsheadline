import feedparser
from flask import Flask

app = Flask(__name__)

RSS_FEEDS = {'toi': 'https://timesofindia.indiatimes.com/rssfeedstopstories.cms',
             'tg': 'https://tj.news/rss/topstories.xml', #telegraph uk
             }

@app.route("/")
@app.route("/<publication>")
def get_news(publication="toi"):
  feed = feedparser.parse(RSS_FEEDS[publication])
  first_article = feed['entries'][3]
  return """<html>
    <body>
        <h1>Headlines </h1>
        <b>{0}</b> </ br>
        <i>{1}</i> </ br>
        <p>{2}</p> </ br>
    </body>
</html>""".format(first_article.get("title"), first_article.get("published"), first_article.get("summary"))


if __name__ == "__main__":
  app.run(port=5000, debug=True)