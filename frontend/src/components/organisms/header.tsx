import { Link } from "react-router-dom";
import { CustomLogo } from "../atoms/custom-logo"
import { SearchBar } from "../molecules/search-bar";
import { CustomIcon } from "../atoms/custom-icon";
import { PlusSquare, ShoppingCart, User } from "lucide-react";
import logoSvg from "../../assets/logo.svg"

interface HeaderProps {
  onSearch?: (query: string) => void;
}

export const Header = ({ onSearch }: HeaderProps) => {

  const handleSearch = (query: string) => {
    if (onSearch) {
      onSearch(query);
    }
  };


  return (
    <header className="w-full bg-black border-b border-zinc-900 sticky top-0 z-50">
      <div className="container mx-auto px-4 h-20 flex items-center justify-between gap-8">
        <Link to="/" className="shrink-0">
          <CustomLogo src={logoSvg} alt="Lojas H1gH" size="md" />
        </Link>

        <div className="flex-1 max-w-2xl hidden md:block">
          <SearchBar onSearch={handleSearch} placeholder="Buscar produtos..." />
        </div>

        <div className="flex flex-col items-center gap-1">
          <div className="flex items-center gap-4 text-white">
            <button className="hover:text-(--color-primary) transition-colors">
              <User size={24} />
            </button>
            <button className="hover:text-(--color-primary) transition-colors relative">
              <ShoppingCart size={24} />
              <span className="absolute -top-2 -right-2 bg-(--color-primary) text-black text-[10px] font-bold px-1.5 rounded-full">
                0
              </span>
            </button>
          </div>

          {/* Botão para Criar Produto posicionado abaixo */}
          <Link
            to="/product/create"
            className="text-[10px] font-black uppercase italic text-zinc-500 hover:text-(--color-primary) transition-colors flex items-center gap-1"
          >
            <PlusSquare size={12} />
            Criar Produto
          </Link>
        </div>

        <div className="md:hidden px-4 pb-4">
          <SearchBar onSearch={handleSearch} />
        </div>
      </div>
    </header>
  );
};
