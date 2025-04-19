import json
from src.services.classifier_service import classify

def classify_all_news():
    with open("src/data/data.json", "r") as f:
        news_data = json.load(f)
    result = []
    for item in news_data:
        result.append({
            "texto": item["texto"],
            "classificacao": classify(item["texto"])
        })
    return result