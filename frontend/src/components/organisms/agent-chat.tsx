import { useState, useRef, useEffect } from "react";
import { MessageSquare, X, Send, Loader2 } from "lucide-react";
import axios from "axios";

type Message = {
  id: number;
  role: "usuário" | "ia";
  text: string;
};

const api = axios.create({
  baseURL: "http://localhost:8000",
});

const loadingMessages = [
  "Analisando sua pergunta...",
  "Explorando o banco de dados...",
  "Cruzando os dados de produtos...",
  "Formatando os resultados...",
  "Quase lá...",
];

export function AgentChat() {
  const [isOpen, setIsOpen] = useState(false);
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false)
  const [loadingMessageIndex, setLoadingMessageIndex] = useState(0);
  const [chatLog, setChatLog] = useState<Message[]>([
    {
      id: 1,
      role: "ia",
      text: "E aí! No que posso te ajudar?",
    },
  ]);

  const mensagensEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (mensagensEndRef.current) {
      mensagensEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [chatLog, isOpen]);

  useEffect(() => {
    let intervalId: ReturnType<typeof setInterval>;

    if (isLoading) {
      setLoadingMessageIndex(0);

      intervalId = setInterval(() => {
        setLoadingMessageIndex((prevIndex) => {
          if (prevIndex < loadingMessages.length - 1) {
            return prevIndex + 1;
          }
          return prevIndex;
        });
      }, 2500);
    }

    return () => clearInterval(intervalId);
  }, [isLoading]);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim() || isLoading) return;

    const userText = message;
    const userNewMessage: Message = {
      id: Date.now(),
      role: "usuário",
      text: userText,
    };

    setChatLog((prev) => [...prev, userNewMessage]);
    setMessage("");
    setIsLoading(true)

    try {
      const response = await api.post("/chat/", {
        question: userText
      })

      const novaMensagemAI: Message = {
        id: Date.now(),
        role: "ia",
        text: response.data.conclusion,
      };

      setChatLog((prev) => [...prev, novaMensagemAI]);
    } 
    catch (err) {
      console.error("Erro ao buscar resposta da IA:", err);
      setChatLog((prev) => [
        ...prev,
        {
          id: Date.now(),
          role: "ia",
          text: "Opa, tivemos um problema de conexão com nossos servidores. Tente novamente mais tarde!",
        },
      ]);
    }
    finally {
      setIsLoading(false)
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end">
      <div
        className={`transition-all duration-300 ease-in-out transform origin-bottom-right ${
          isOpen ? "scale-100 opacity-100 mb-4" : "scale-0 opacity-0 h-0 w-0"
        }`}
      >
        <div className="w-80 sm:w-96 h-120 bg-zinc-950 border border-zinc-800 rounded-xl shadow-2xl flex flex-col overflow-hidden">
          <div className="bg-zinc-900 border-b border-zinc-800 p-4 flex justify-between items-center">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-(--color-primary) animate-pulse"></div>
              <h3 className="text-zinc-100 font-bold uppercase tracking-wider text-sm">
                Suporte AI
              </h3>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="text-zinc-400 hover:text-zinc-100 transition-colors"
            >
              <X size={20} />
            </button>
          </div>

          <div className="flex-1 p-4 overflow-y-auto space-y-4 scrollbar-thin scrollbar-thumb-zinc-700 scrollbar-track-transparent">
            {chatLog.map((msg) => (
              <div
                key={msg.id}
                className={`flex ${msg.role === "usuário" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-[80%] rounded-2xl px-4 py-2 text-sm ${
                    msg.role === "usuário"
                      ? "bg-(--color-primary) text-white rounded-br-none"
                      : "bg-zinc-800 text-zinc-300 rounded-bl-none border border-zinc-700"
                  }`}
                >
                  {msg.text}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-zinc-800 text-zinc-400 rounded-2xl rounded-bl-none border border-zinc-700 px-4 py-2 text-sm flex items-center gap-2">
                  <Loader2 size={14} className="animate-spin" />
                  <span className="animate-pulse">
                    {loadingMessages[loadingMessageIndex]}
                  </span>
                </div>
              </div>
            )}
            <div ref={mensagensEndRef} />
          </div>

          <form
            onSubmit={sendMessage}
            className="p-3 bg-zinc-900 border-t border-zinc-800 flex items-center gap-2"
          >
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Digite sua dúvida..."
              className="flex-1 bg-zinc-950 border border-zinc-700 text-zinc-100 text-sm rounded-lg px-4 py-2.5 focus:outline-none focus:border-(--color-primary-hover) focus:ring-1 focus:ring-(--color-primary-hover) transition-all placeholder:text-zinc-600"
            />
            <button
              type="submit"
              disabled={!message.trim()}
              className="bg-(--color-primary) hover:bg-(--color-primary-hover) disabled:opacity-50 disabled:hover:bg-(--color-primary-hover) text-white p-2.5 rounded-lg transition-colors flex items-center justify-center"
            >
              <Send size={18} />
            </button>
          </form>
        </div>
      </div>

      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`p-4 rounded-full shadow-lg transition-all duration-300 flex items-center justify-center ${
          isOpen
            ? "bg-zinc-800 text-zinc-400 hover:bg-zinc-700"
            : "bg-(--color-primary) text-white hover:bg-(--color-primary-hover) hover:scale-105"
        }`}
      >
        {isOpen ? <X size={24} /> : <MessageSquare size={24} />}
      </button>
    </div>
  );
}
