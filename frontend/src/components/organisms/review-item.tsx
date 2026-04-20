import { type Review } from "../../models/avaliacao.model";
import { Star } from "lucide-react";

interface ReviewItemPros {
  review: Review;
}

export const ReviewItem = ({ review }: ReviewItemPros) => {
  // Função simples para renderizar as estrelas baseadas na nota
  const renderStars = (rating: number) => {
    return Array.from({ length: 5 }).map((_, i) => (
      <Star
        key={i}
        size={14}
        className={
          i < rating
            ? "fill-(--color-primary) text-(--color-primary)"
            : "text-zinc-700"
        }
      />
    ));
  };

  return (
    <div className="bg-[#111] border border-zinc-900 p-6 flex flex-col gap-4">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-2">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-zinc-800 flex items-center justify-center rounded-none border border-zinc-700">
            <span className="text-zinc-400 font-bold text-xs uppercase">
              {review.nome_consumidor.substring(0, 2)}
            </span>
          </div>
          <div>
            <h4 className="text-white font-bold text-sm uppercase italic tracking-tighter">
              {review.nome_consumidor}
            </h4>
            <div className="flex gap-0.5 mt-0.5">
              {renderStars(review.avaliacao)}
            </div>
          </div>
        </div>

        <span className="text-zinc-500 text-[10px] font-mono uppercase">
          {new Date(review.data_comentario).toLocaleDateString("pt-BR")}
        </span>
      </div>

      <div className="flex flex-col gap-1">
        <h5 className="text-(--color-primary) font-black text-sm uppercase italic tracking-tight">
          {review.titulo_comentario}
        </h5>
        <p className="text-zinc-400 text-sm leading-relaxed">
          {review.comentario}
        </p>
      </div>
    </div>
  );
};
