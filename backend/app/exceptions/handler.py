from fastapi import Request
from fastapi.responses import JSONResponse

async def rate_limit_exception_handler(request: Request, exc: Exception):
  return JSONResponse(
    status_code=429,
    content={"detail": "Limite de tokens atingido. Tente novamente mais tarde."},
  )

async def global_exception_handler(request: Request, exc: Exception):
  return JSONResponse(
    status_code=500,
    content={"detail": "Ocorreu um erro interno no servidor."},
  )
