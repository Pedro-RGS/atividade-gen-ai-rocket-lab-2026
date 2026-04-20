import asyncio
import json
import sys
from pathlib import Path

from dotenv import load_dotenv
from pydantic_ai.messages import FunctionToolCallEvent, FunctionToolResultEvent

load_dotenv()

from src.agents.agent import Deps, agent
from src.utils.db import DatabaseManager
from src.agents.judge_agent import evaluate_interaction

def _format_args(args: str | dict) -> str:
  if isinstance(args, str):
    try: 
      args = json.loads(args)
    except Exception:
      return args
  
  return json.dumps(args, ensure_ascii=False, indent=4)

def _indent(text: str, spaces: int) -> str:
    pad = " " * spaces
    return "\n".join(pad + line for line in text.splitlines())

async def run_agent(question: str, db: DatabaseManager, message_history: list) -> list:
  deps = Deps(db=db)
  step = 0
  executed_sqls: list[str] = []

  print("\n" + "─" * 60)
  print(f"  Analisando: {question}")
  print("─" * 60)

  try:
    async with agent.iter(question, deps=deps, message_history=message_history) as run:
      async for node in run:

        if agent.is_call_tools_node(node):
          async with node.stream(run.ctx) as tool_stream:
            async for event in tool_stream:

              if isinstance(event, FunctionToolCallEvent):
                step += 1
                args_str = _format_args(event.part.args)
                print(f"\n  [Passo {step}] Chamando: {event.part.tool_name}")
                print(f"     Args:\n{_indent(args_str, 9)}")

                if event.part.tool_name == "run_sql_query":
                  raw = event.part.args
                  if isinstance(raw, str):
                    raw = json.loads(raw)
                  if isinstance(raw, dict) and "sql" in raw:
                    executed_sqls.append(raw["sql"])
              
              elif isinstance(event, FunctionToolResultEvent):
                content = event.result.content
                preview = content[:400] + \
                    ("  [...]" if len(content) > 400 else "")
                print(f"  Resultado:\n{_indent(preview, 9)}")
        result = run.result
    
    output = result.output
    print("\n" + "=" * 60)
    print("  CONCLUSÃO DO ANALISTA:")
    print("-" * 60)
    print(output.conclusion)

    sqls_for_judge = executed_sqls.copy()

    if executed_sqls:
      print("-" * 60)
      print("  SQLs executados (na ordem):")
      for i, sql in enumerate(executed_sqls, 1):
        print(f"  [{i}] {sql}")
      print("=" * 60)
    
    print("\n Avaliação de qualidade:")
    try:
      review = await evaluate_interaction(question, sqls_for_judge, output.conclusion)
      is_safe_str = "✅ Seguro (Apenas Leitura)" if review.is_safe else "❌ INSEGURO (Alerta Crítico)"
      print("   ╭─── BOLETIM DE QUALIDADE ─────────────────")
      print(f"  │ Nota Técnica: {review.score}/100")
      print(f"  │ Segurança:    {is_safe_str}")
      print(f"  │ Feedback:     {review.feedback}")
      print("   ╰──────────────────────────────────────────\n")
    
    except Exception as e:
      print(f"  │ Erro ao gerar avaliação: {e}")
      print("  ╰──────────────────────────────────────────\n")
    
    return message_history + result.new_messages()
  
  except Exception as e:
    error_type = type(e).__name__
    print(f"\n  !!! Erro ao processar a pergunta ({error_type}): {e}")
    print("  O histórico da conversa foi preservado. Tente novamente.")
    
    return message_history

DB_PATH = Path(__file__).parent / "banco.db"

async def main() -> None:
  db = DatabaseManager(db_path=DB_PATH)

  message_history: list = []

  try:
    if len(sys.argv) > 1:
      question = " ".join(sys.argv[1:])
      await run_agent(question, db, message_history)
      return

    print("╔══════════════════════════════════════════════════════════╗")
    print("║           Agente Analista de Dados E-commerce            ║")
    print("╠══════════════════════════════════════════════════════════╣")
    print("║  • O agente mostrará cada passo que ele toma (ReACT)     ║")
    print("║  • O contexto da conversa é mantido entre perguntas      ║")
    print("║  • Digite 'sair', 'exit' ou 'q' para encerrar            ║")
    print("╚══════════════════════════════════════════════════════════╝\n")

    while True:
      question = input("\nPergunta: ").strip()
      if question.lower() in ("sair", "exit", "quit", "q"):
        print("Até mais!")
        break
      if not question:
        continue

      try:
        message_history = await run_agent(question, db, message_history)
      except Exception as e:
        print(f"\n  !!!Erro inesperado: {type(e).__name__}: {e}")
        print("  O histórico foi preservado. Continue perguntando.")
  finally:
    db.close_db()

if __name__ == "__main__":
  asyncio.run(main())