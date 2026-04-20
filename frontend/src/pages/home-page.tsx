import { MainLayout } from "../components/templates/main-layout";
import type { ProductCardModel } from "../models/produto-card.model";
import { useEffect, useState } from "react";
import { ItemCard } from "../components/molecules/item-card";
import { CustomButton } from "../components/atoms/custom-button";
import { CATEGORIES_DATA } from "../models/categorias"
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

export const HomePage = () => {
  const [products, setProducts] = useState<ProductCardModel[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("");

  const limit = 10;

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        const offset = (page - 1) * limit;

        const response = await api.get("/produtos", {
          params: {
            limit,
            offset,
            name: searchTerm,
            category: selectedCategory,
          },
        });

        console.log("Resposta da API:", response.data);

        if (response.data) {
          setProducts(response.data.data || []);
          setTotalPages(response.data.meta?.total_pages || 1);
        }
      } catch (err) {
        console.error("Error fetching products:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchProducts();
  }, [page, searchTerm, selectedCategory]);

  const handleSearch = (query: string) => {
    setSearchTerm(query);
    setPage(1);
  };

  const handleCategoryChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedCategory(e.target.value);
    setPage(1);
  };

  return (
    <MainLayout onSearch={handleSearch}>
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold mb-6 text-(--color-primary)">
          Nossos Produtos
        </h1>

        <div className="flex items-center gap-2">
            <label htmlFor="category-filter" className="text-sm font-medium text-gray-400">
              Filtrar por:
            </label>
            <select
              id="category-filter"
              value={selectedCategory}
              onChange={handleCategoryChange}
              className="bg-[#111] text-white border border-zinc-800 rounded px-3 py-2 focus:outline-none focus:border-(--color-primary) min-w-[200px]"
            >
              <option value="">Todas as Categorias</option>
              {CATEGORIES_DATA.filter(c => c.value !== "").map((cat) => (
                <option key={cat.value} value={cat.value}>
                  {cat.label}
                </option>
              ))}
            </select>
        </div>

        <div className="flex justify-center items-center gap-4 mb-5">
          <CustomButton
            onClick={() => setPage((prev) => Math.max(prev - 1, 1))}
            disabled={page === 1 || loading}
            variant="secondary"
          >
            Anterior
          </CustomButton>

          <span className="font-medium text-gray-700">
            Página {page} de {totalPages}
          </span>

          <CustomButton
            onClick={() => setPage((prev) => prev + 1)}
            disabled={page >= totalPages || loading}
            variant="secondary"
          >
            Próxima
          </CustomButton>
        </div>

        {loading ? (
          <div className="text-center py-10">Carregando...</div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {products.map((product) => (
              <ItemCard
                key={product.id_produto}
                id={product.id_produto}
                name_product={product.nome_produto}
                category={product.categoria_produto}
                price={product.preco}
                url_image={product.url_imagem}
              />
            ))}
          </div>
        )}
      </div>
    </MainLayout>
  );
};
