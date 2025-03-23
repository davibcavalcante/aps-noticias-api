import feedparser
from src.config import FEED_URL
from src.models.rss_model import RSSFeed, RSSItem

def get_rss_feed():
    feed = feedparser.parse(FEED_URL)
    if feed.bozo:
        return None

    return RSSFeed(
        title=feed.feed.get("title", "Sem título"),
        link=feed.feed.get("link", "Sem link"),
        description=feed.feed.get("description", "Sem descrição"),
        items=[
            RSSItem(
                title=entry.get("title", "Sem título"),
                link=entry.get("link", "Sem link"),
                published=entry.get("published", "Sem data"),
                summary=entry.get("summary", "Sem resumo"),
                image=entry.get("imagem-destaque", "sem imagem"),
            )
            for entry in feed.entries
        ],
    )
