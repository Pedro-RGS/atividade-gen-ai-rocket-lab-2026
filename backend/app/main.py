from fastapi import FastAPI
from app.routes import produtos_routes, avaliacoes_pedido_routes, agent_routes
from fastapi.middleware.cors import CORSMiddleware
from app.exceptions.handler import global_exception_handler, rate_limit_exception_handler
from pydantic_ai import ModelHTTPError

app = FastAPI(
    title="Sistema de Compras Online",
    description="API para gerenciamento de pedidos, produtos, consumidores e vendedores.",
    version="1.0.0",
)

origins = [
    "http://localhost:5173",  # Porta padrão do Vite/React
    "http://localhost:3000",  # Porta padrão do Create React App
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(ModelHTTPError, rate_limit_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)
app.include_router(produtos_routes.router)
app.include_router(avaliacoes_pedido_routes.router)
app.include_router(agent_routes.router)

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "API rodando com sucesso!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
