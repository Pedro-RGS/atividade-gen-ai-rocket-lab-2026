from pydantic import BaseModel, Field

class AgentResponseSchema(BaseModel):
  conclusion: str = Field(
    ...,
    description="O texto explicativo com a resposta da análise de dados.",
    example="Com base na análise, o produto mais vendido foi o iPhone 15."
  )
