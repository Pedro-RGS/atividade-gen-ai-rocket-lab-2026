from dataclasses import dataclass
from datetime import date
from typing import Annotated

from annotated_types import MinLen
from pydantic import BaseModel, Field
from pydantic_ai import Agent, ModelRetry, RunContext

from app.utils.db import DatabaseManager

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
  "google-gla:gemini-2.5-flash",
  output_type=AnalystResult,
  deps_type=Deps,
  retries=3
)

@agent.system_prompt
async def system_prompt(ctx: RunContext[Deps]) -> str:
  schema = ctx.deps.db.list_tables()

  return f"""\
Você é um analista de dados especialista em bancos de dados SQLite de sistemas de E-commerce.
Sua missão é analisar a pergunta do usuário, traduzi-la para uma query SQLite e responder com insights precisos baseados estritamente nos dados reais.

REGRAS CRÍTICAS:
1. Você tem apenas a lista de tabelas. Você DEVE usar a ferramenta `describe_tables` para entender as colunas de uma tabela antes de montar qualquer query.
2. É ESTRITAMENTE PROIBIDO deduzir ou "chutar" valores para filtros de texto/booleanos (ex: 'true', 'Sim', 'Atrasado').
3. Você DEVE obrigatoriamente usar a ferramenta `get_distinct_values` ANTES de fazer qualquer filtro (WHERE, HAVING ou CASE WHEN) em colunas de texto/status para descobrir a grafia exata no banco.
4. Você DEVE criar uma query SELECT e executá-la chamando a ferramenta `run_sql_query`.
5. SEMPRE inclua LIMIT nas consultas SQL iniciais exploratórias para evitar logs gigantes.
6. Se a consulta retornar 0 linhas, não invente dados. Tente flexibilizar seus filtros.
7. Após examinar os dados reais, formule sua saída final na variável `conclusion`.

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
  """
  Retorna o DDL (CREATE TABLE) de uma tabela específica
  Use essa ferramenta ANTES de escrever a query final (SELECT) para verificar
  os tipos de dados de cada coluna de uma tabela específica
  """
  return ctx.deps.db.describe_tables(table_name)

@agent.tool
async def get_distinct_values(ctx: RunContext[Deps], table_name: str, column_name: str) -> str:
  """
  Retorna até 30 valores únicos (DISTINCT) de uma coluna específica em uma tabela.
  USE ESTA FERRAMENTA ANTES de escrever a query final (SELECT) se você tiver dúvidas 
  sobre quais categorias existem ou qual é a grafia exata dos dados.
  """
  
  unique_values = ctx.deps.db.get_distinct_values(table_name, column_name)
  formatted_values = ", ".join(map(str, unique_values))

  return f"Valores únicos na coluna '{column_name}' na tabela '{table_name}': {formatted_values}"
