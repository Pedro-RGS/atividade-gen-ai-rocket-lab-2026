import sqlite3
from pathlib import Path
from typing import Any

class DatabaseManager:

  def __init__(self, db_path: str | Path):
    self.db_path = str(db_path)
    self.conn = sqlite3.connect(self.db_path)
    self.conn.row_factory = sqlite3.Row
  
  def list_tables(self) -> list[str]:
    cursor = self.conn.execute(
      "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )
    return [row['name'] for row in cursor.fetchall()]
  
  def get_full_schema(self) -> str:
    tables = self.list_tables()
    schemas = [self.describe_tables(t) for t in tables]
    return "\n\n".join(schemas)
  
  def describe_tables(self, table_name: str) -> str:
    cursor = self.conn.execute(
      "SELECT sql FROM sqlite_master WHERE type='table' AND name=?",
      (table_name,),
    )

    row = cursor.fetchone()

    if row is None:
      return f"Nenhuma tabela com nome {table_name} foi encontrada no schema"
    
    return row["sql"]
  
  def run_query(self, query: str, limit: int = 20) -> list[dict]:
    treated_query = query.strip().upper()
    
    # Validações para a query não quebrar o banco com consultas que não são SELECT
    # caso não seja uma query de leitura ele para o agente por segurança
    if not treated_query.startswith("SELECT") and not treated_query.startswith("WITH"):
      raise ValueError("Erro: Apenas consultas de leitura são permitidas")
    
    # Força o LIMIT na query para não gastar muitos tokens
    if "LIMIT" not in treated_query:
      query = f"{query.rstrip(';')} LIMIT {limit}"

    cursor = self.conn.execute(query)
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    return [dict(zip(columns, row)) for row in rows]
  
  def validate_sql(self, query: str) -> tuple[bool, str]:
    try:
      self.conn.execute(f"EXPLAIN {query}")
      return True, "OK"
    
    except sqlite3.Error as e:
      return False, str(e)
    
  # Nova função para o agente obter os valores distintos de uma coluna em uma tabela
  def get_distinct_values(self, table_name: str, column_name: str) -> list[Any]:
    try:
      cursor = self.conn.execute(
        f"SELECT DISTINCT {column_name} FROM {table_name} WHERE {column_name} IS NOT NULL LIMIT 30"
      )
      return [row[0] for row in cursor.fetchall()]

    except sqlite3.Error as e:
      return [f"Erro: {e}"]

  def close_db(self):
    self.conn.close()