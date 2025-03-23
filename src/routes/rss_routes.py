from fastapi import APIRouter
from src.controllers.rss_controller import fetch_rss

router = APIRouter()

@router.get("/rss/", tags=["RSS"])
def read_rss():
    return fetch_rss()

@router.get('/')
def teste_route():
    return "Hello, World"
