import { EditIcon } from "lucide-react";
import { CustomImage } from "../atoms/custom-image";
import { Link } from "react-router-dom";

interface ItemCardProps {
  id: string;
  name_product: string;
  category: string;
  price: number;
  url_image: string;
}

export const ItemCard = ({
  id,
  name_product,
  category,
  price,
  url_image,
}: ItemCardProps) => {
  const formattedPrice = new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(price);

  return (
    <Link
      to={`/product/${id}`}
      className="group flex flex-col bg-[#111111] border border-zinc-900 overflow-hidden transition-all hover:border-zinc-700 w-full"
    >
      <div className="aspect-square w-full bg-[#1a1a1a] overflow-hidden p-8">
        <CustomImage
          src={url_image}
          alt={name_product}
          className="w-full h-full group-hover:scale-105 transition-transform duration-500"
        />
      </div>

      <Link to={`/admin/editar-produto/${id}`}>
        <EditIcon size={18} className="text-zinc-400 hover:text-white" />
      </Link>

      <div className="p-4 flex flex-col gap-1">
        <span className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest">
          {category}
        </span>
        <h3 className="text-[13px] font-bold text-white line-clamp-2 leading-tight uppercase group-hover:text-(--color-primary) transition-colors">
          {name_product}
        </h3>
        <div className="mt-3">
          <span className="text-xl font-black text-(--color-primary)">
            {formattedPrice}
          </span>
        </div>
      </div>
    </Link>
  );
};