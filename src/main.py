from fastapi import FastAPI
from src.routes import rss_routes, classify_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="RSS API", description="API para consumir um feed RSS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

@app.get("/test")
async def test():
    return {"message": "API está funcionando!"}

app.include_router(rss_routes.router, prefix="/api/rss")
app.include_router(classify_routes.router, prefix="/api/classify")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)