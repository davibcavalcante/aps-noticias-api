from fastapi import HTTPException
from src.services.rss_service import get_rss_feed

def fetch_rss():
    feed_data = get_rss_feed()
    
    if not feed_data:
        raise HTTPException(status_code=500, detail="Erro ao processar o feed RSS.")

    return feed_data
