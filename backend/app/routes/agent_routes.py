import os
from pathlib import Path
from fastapi import APIRouter, status
from app.config import DB_PATH
from app.agent.main import agent, Deps
from app.utils.db import DatabaseManager
from app.schemas.agent_schema import AgentResponseSchema, AgentRequestSchema


router = APIRouter(
    prefix="/chat",
    tags=["Agente"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AgentResponseSchema)
async def chat_with_ai(question: AgentRequestSchema):
  db_manager = DatabaseManager(db_path=DB_PATH)

  try:
    result = await agent.run(question.question, deps=Deps(db=db_manager))
    return {"conclusion": result.output.conclusion}
  
  finally:
    db_manager.close_db()
