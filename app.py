import feedparser
from flask import Flask, jsonify, send_from_directory
import os

app = Flask(__name__)
feeds = []


def parse_rss(feed_url):
    return feedparser.parse(feed_url)


def correlate_articles(feed_urls):
    all_articles = []

    for feed_url in feed_urls:
        feed = feedparser.parse(feed_url)

        # Extract channel information
        channel_info = {
            "channel_title": feed.feed.get("title", "No Title"),
            "channel_link": feed.feed.get("link", ""),
            "channel_image": feed.feed.get("image", {}).get("href", "")
        }

        # Correlate articles by pubDate and include additional fields
        for entry in feed.entries:
            content = ''

            if entry.get("content"):
                if entry.get("content")[0]:
                    content = entry.get("content")[0].value

            article = {
                "channel_title": channel_info["channel_title"],
                "channel_link": channel_info["channel_link"],
                "channel_image": channel_info["channel_image"],
                "article_title": entry.get("title", "No Title"),
                "article_link": entry.get("link", ""),
                "article_body": content,
                "article_description": entry.get("description", "No Description"),
                "article_pubDate": entry.get("published", ""),
                "article_images": []
            }

            # Look for any images (commonly in media:content or other image tags)
            if "media_content" in entry:
                for media in entry.media_content:
                    if media.get("medium") == "image":
                        article["article_images"].append(media.get("url"))
                    if media.get("expression") == "full":
                        article["article_images"].append(media.get("url"))
            elif "media_thumbnail" in entry:
                for media in entry.media_thumbnail:
                    article["article_images"].append(media.get("url"))

            all_articles.append(article)

    # Sort articles by pubDate
    all_articles.sort(key=lambda x: x["article_pubDate"], reverse=True)

    return all_articles


def load_rss_feeds():
    print("Loading RSS Feeds")
    feed_file = 'feeds.txt'
    if not os.path.exists(feed_file):
        print("Feed file not found")

    with open(feed_file, 'r') as f:
        urls = f.readlines()
        for url in urls:
            feed = parse_rss(url.strip())
            if feed:
                feeds.append(url)
    return feeds


# Serve the index.html directly from the static folder
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


# API to return RSS articles
@app.route('/api/rss', methods=['GET'])
def get_rss_articles():
    correlated_articles = correlate_articles(feeds)
    return jsonify(correlated_articles)


if __name__ == '__main__':
    load_rss_feeds()
    app.run(host='0.0.0.0')
