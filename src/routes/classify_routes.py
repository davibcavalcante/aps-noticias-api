from fastapi import APIRouter, Query, HTTPException
from src.nlp.predict import predict_class, classify_all
from src.nlp.train import train_model
from pydantic import BaseModel

router = APIRouter()

class TextRequest(BaseModel):
    text: str

@router.post("/classify")
def classify_text(request: TextRequest):
    try:
        classification = predict_class(request.text)
        return {"text": request.text, "result": classification, "message": "Notícia classificada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/classify-all")
def classify_all_news():
    try:
        results = classify_all()
        return {"results": results, "message": "Notícias classificadas com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/train")
def trigger_training():
    try:
        train_model()
        return {"message": "Treinamento concluído com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))