from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/protocol", tags=["rede"])
def read_protocol(request: Request):
    client_host = request.client.host
    http_version = request.scope.get("http_version", "unknown")
    scheme = request.url.scheme
    
    return { "ip": client_host, "version": http_version, "scheme": scheme }