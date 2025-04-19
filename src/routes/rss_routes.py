from fastapi import APIRouter
from src.controllers.rss_controller import fetch_rss

router = APIRouter()

@router.get("/list", tags=["RSS"])
def read_rss():
    return fetch_rss()
