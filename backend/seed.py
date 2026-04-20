import pandas as pd
from app.database import SessionLocal
from sqlalchemy import insert

from app.models.avaliacao_pedido import AvaliacaoPedido
from app.models.consumidor import Consumidor
from app.models.item_pedido import ItemPedido
from app.models.produto import Produto
from app.models.vendedor import Vendedor
from app.models.pedido import Pedido
from app.models.categoria_imagem import CategoriaImagem

def seed_database():
  db = SessionLocal()
  base_path = "..\\csv-database-files\\"

  mapping = [
      {"file": "dim_consumidores.csv", "model": Consumidor},
      {"file": "dim_produtos.csv", "model": Produto},
      {"file": "dim_vendedores.csv", "model": Vendedor},
      {"file": "fat_itens_pedidos.csv", "model": ItemPedido},
      {"file": "fat_avaliacoes_pedidos.csv", "model": AvaliacaoPedido},
      {"file": "fat_pedidos.csv", "model": Pedido},
      {"file": "dim_categoria_imagens.csv", "model": CategoriaImagem}
    ]
  try:
    for item in mapping:
      file_path = base_path + item["file"]
      model = item["model"]

      df = pd.read_csv(file_path)

      # Limpando dados duplicados no fat_avaliacoes_pedidos
      if item["file"] == "fat_avaliacoes_pedidos.csv":
        df = df.drop_duplicates(subset=["id_avaliacao"])

      date_columns = [
        "pedido_compra_timestamp",
        "pedido_entregue_timestamp",
        "data_estimada_entrega",
        "data_comentario",
        "data_resposta",
      ]

      # Tratamento de colunas de data para converte-las em objetos de data do python
      for col in date_columns:
        if col in df.columns:
          df[col] = pd.to_datetime(df[col], errors="coerce")


      df = df.where(pd.notnull(df), None)

      data = df.to_dict(orient="records")

      for record in data:
        for key, value in record.items():
          if pd.isna(value): 
            record[key] = None
          elif isinstance(value, pd.Timestamp):
            record[key] = value.to_pydatetime()
          elif isinstance(value, float):
            if value.is_integer():
              record[key] = int(value)

      db.execute(insert(model), data)
      db.commit()

      print("Data inserted successfully for:", item["file"])

  except Exception as e:
    db.rollback()
    print("Error:", e)

  finally:
    db.close()

if __name__ == "__main__":
  seed_database()