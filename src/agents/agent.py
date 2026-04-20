from dataclasses import dataclass
from datetime import date
from typing import Annotated

from annotated_types import MinLen
from pydantic import BaseModel, Field
from pydantic_ai import Agent, ModelRetry, RunContext

from src.utils.db import DatabaseManager

@dataclass
class Deps:
  """Dependências injetadas no agente via RunContext"""
  db: DatabaseManager

class AnalystResult(BaseModel):
  """
  Resultado final da análise de dados.
  Este objeto contém a resposta definitiva que será exibida para o usuário, 
  baseada estritamente nas evidências encontradas no banco de dados.
  """
  conclusion: Annotated[str, MinLen(10)] = Field(
      ..., description="""Conclusão textual e explicativa gerada a partir da análise dos
        dados retornados, respondendo efetivamente a pergunta do usuário."""
  )

agent = Agent(
  "google-gla:gemini-2.5-flash-lite",
  output_type=AnalystResult,
  deps_type=Deps,
  retries=3
)

@agent.system_prompt
async def system_prompt(ctx: RunContext[Deps]) -> str:
  schema = ctx.deps.db.get_full_schema()

  return f"""\
Você é um analista de dados especialista em bancos de dados SQLite de sistemas de E-commerce
Sua missão é analisar a pergunta do usuário, traduzi-la para uma query SQLite e responder com insights precisos baseados estritamente no schema passado

REGRAS CRÍTICAS:
1. Você DEVE realizar APENAS consultas sql.
2. Você DEVE criar uma query SELECT baseada no schema fornecido.
3. Você DEVE obrigatoriamente executar essa query no banco chamando a ferramenta `run_sql_query`.
4. Você DEVE SEMPRE verificar os dados que estão na coluna.
4. Você NUNCA deve tentar deduzir ou 'chutar' resultados.
5. Você DEVE observar o retorno da ferramenta.
6. Após examinar os dados, formule sua saída final (AnalystResult) contendo a conclusão descritiva (`conclusion`).
7. SEMPRE inclua LIMIT nas consultas sql iniciai se estiver incerto para evitar logs com dezenas de MBs.
8. Se a consulta retornar 0 linhas ou valores zerados, não invente dados. Reveja seus filtros.
9. Se a consulta retornar 0 linhas, não invente dados. Explique para o usuário de forma clara que não foram encontrados registros para o que ele pediu

Schema do banco de dados:
{schema} 

Data de hoje: {date.today()}

"""

@agent.tool
async def run_sql_query(ctx: RunContext[Deps], sql: str) -> str:
  """
  Executa uma query no banco de dados SQLite e retorna as linhas de dados em texto puro.
  Você DEVE usar esta ferramenta antes de gerar qualquer conclusão relacionada aos dados.
  """
  
  if not sql.strip().upper().startswith("SELECT"):
    raise ModelRetry("Por segurança, use apenas queries de leitura (SELECT).")
  
  try:
    rows = ctx.deps.db.run_query(sql)

    if not rows:
      return "A query retornou 0 linhas, tente flexibilizar os filtros ou verificar as colunas disponíveis."
    
    import json
    if len(rows) > 30:
      preview = rows[:30]
      minified_preview = json.dumps(preview, default=str, separators=(',', ':'))
      return f"30 resultados de {len(rows)} totais: {minified_preview}\n[Use LIMIT se precisar de mais.]"
    
    return json.dumps(rows, default=str, separators=(',', ':'))

  except Exception as e:
    raise ModelRetry(f"Sua query falhou no SQLite: {e}. Altere sua query baseada no schema e tente de novo")

@agent.tool
async def list_tables(ctx: RunContext[Deps]) -> str:
  """
  Lista todas as tabelas disponíveis no banco de dados.
  Use essa ferramenta para saber quais são as tabelas existentes no banco de dados
  """
  tables = ctx.deps.db.list_tables()
  return ", ".join(tables)

@agent.tool
async def describe_tables(ctx: RunContext[Deps], table_name: str) -> str:
  """Retorna o DDL (CREATE TABLE) de uma tabela específica"""
  return ctx.deps.db.describe_tables(table_name)

@agent.tool
async def get_distinct_values(ctx: RunContext[Deps], table_name: str, column_name: str) -> str:
  """
  Retorna até 30 valores únicos (DISTINCT) de uma coluna específica em uma tabela.
  USE ESTA FERRAMENTA ANTES de escrever a query final (SELECT) se você tiver dúvidas 
  sobre quais categorias existem ou qual é a grafia exata dos dados.
  """
  
  unique_values = ctx.deps.db.get_distinct_values(table_name, column_name)
  formated_values = ", ".join(map(str, unique_values))

  return f"Valores únicos na coluna '{column_name}' na tabela '{table_name}': {formated_values}"
