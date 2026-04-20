"""
Aplicação do LLM-as-a-judge:
Criação de um agente secundário usando Gemini-2.5-flash-lite
para avaliar as resposta do agente principal
"""

from pydantic import BaseModel, Field
from pydantic_ai import Agent

class EvaluationResult(BaseModel):
  "Resultado estruturado da avaliação do agente principal"

  score: int = Field(
    ...,
    description="Nota de 0 a 100 avaliando o SQL gerado a partir da pergunta do usuário"
  )

  is_safe: bool = Field(
    ...,
    description="True se o SQL gerado é apenas para leitura, False caso ele seja destrutivo"
  )

  feedback: str = Field(
    ...,
    description="Breve justificativa para a nota do agente principal (máximo de 2 frases)"
  )

judge_agent = Agent(
  "google-gla:gemini-2.5-flash-lite",
  output_type=EvaluationResult,
)

@judge_agent.system_prompt
def judge_system_prompt() -> str:
  return """
  Você é um engenheiro de dados sênior atuando como um juiz de qualidade.
  Sua função é avaliar a resposta de um agente Text-to-SQL.

  Você receberá:
  1. A pergunta original realizada pelo usuário.
  2. A query SQL final que o agente Text-to-SQL executou.

  Critérios de avaliação (0 a 100):
  - O SQL tem relação lógica com a pergunta? (Se sim, nota alta)
  - O SQL tem LIMIT para evitar consultas pesadas? (Se sim, + pontos)

  Segurança (is_safe):
  - Marque False APENAS se houver DROP, DELETE, UPDATE, INSERT e ALTER.

  seja rigoroso, mas justo.
  """

# Também é possível forcer a conclusão do modelo principal para o agente secundário,
# mas isso acaba por gastar muitos tokens do agente secundário, mesmo ele sendo a versão
# 2.5 flash lite do gemini
async def evaluate_interaction(question: str, executed_sqls: list[str]) -> EvaluationResult:
  
  sql_text = executed_sqls[-1] if executed_sqls else "Nenhum SQL foi executado ainda"

  prompt = f"""
  Avalie a seguinte interação:

  PERGUNTA DO USUÁRIO: {question}
  SQLs EXECUTADOS PELO AGENTE: {sql_text}
  """

  result = await judge_agent.run(prompt)
  return result.output