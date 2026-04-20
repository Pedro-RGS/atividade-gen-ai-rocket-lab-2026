import axios from "axios";
import { MainLayout } from "../components/templates/main-layout";
import { CustomImage } from "../components/atoms/custom-image";
import { type ProductDetailsModel } from "../models/produto-details.model";
import { type Review } from "../models/avaliacao.model";
import { ReviewItem } from "../components/organisms/review-item";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Trash2 } from "lucide-react";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

export const ProductPage = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [product, setProduct] = useState<ProductDetailsModel>();
  const [reviews, setReviews] = useState<Review[]>([]);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [loadingProduct, setLoadingProduct] = useState(true);
  const [loadingReviews, setLoadingReviews] = useState(true);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        setLoadingProduct(true);
        const response = await api.get(`/produtos/${id}`);
        setProduct(response.data);
      } catch (err) {
        console.error("Erro ao carregar produto:", err);
      } finally {
        setLoadingProduct(false);
      }
    };

    const fetchReviews = async () => {
      try {
        setLoadingReviews(true);
        const response = await api.get(`/avaliacoes/${id}`);
        const { data = [] } = response.data || {};
        setReviews(data);
      } catch (err) {
        console.error("Erro ao carregar avaliações:", err);
      } finally {
        setLoadingReviews(false);
      }
    };

    if (id) {
      fetchProduct();
      fetchReviews();
    }
  }, [id]);

  if (loadingProduct)
    return (
      <MainLayout>
        <div className="text-center py-20 text-white font-black italic uppercase tracking-widest">
          Carregando Produto...
        </div>
      </MainLayout>
    );

  if (!product)
    return (
      <MainLayout>
        <div className="text-center py-20 text-white uppercase font-bold">
          Produto não encontrado.
        </div>
      </MainLayout>
    );

  const handleDelete = async () => {
    try {
      setIsDeleting(true);
      await api.delete(`/produtos/${id}`);

      navigate("/");
    } catch (err) {
      console.error("Erro ao deletar produto:", err);
      alert("Não foi possível deletar o produto.");
    } finally {
      setIsDeleting(false);
      setShowDeleteModal(false);
    }
  };

  return (
    <MainLayout>
      {showDeleteModal && (
        <div className="fixed inset-0 z-100 flex items-center justify-center bg-black/80 backdrop-blur-sm px-4">
          <div className="bg-[#111] border border-zinc-800 p-8 max-w-md w-full shadow-2xl">
            <h2 className="text-white text-xl font-black uppercase italic mb-4">
              Confirmar Exclusão
            </h2>
            <p className="text-zinc-400 mb-8">
              Você tem certeza que deseja remover{" "}
              <span className="text-white font-bold">
                {product.nome_produto}
              </span>{" "}
              do catálogo? Esta ação não pode ser desfeita.
            </p>
            <div className="flex gap-4">
              <button
                onClick={() => setShowDeleteModal(false)}
                className="flex-1 py-3 bg-zinc-800 text-white font-bold uppercase text-xs hover:bg-zinc-700 transition-colors"
              >
                Cancelar
              </button>
              <button
                onClick={handleDelete}
                disabled={isDeleting}
                className="flex-1 py-3 bg-red-600 text-white font-bold uppercase text-xs hover:bg-red-700 transition-colors disabled:opacity-50"
              >
                {isDeleting ? "Deletando..." : "Sim, Deletar"}
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="container mx-auto px-4 py-12 grid grid-cols-1 md:grid-cols-2 gap-12">
        <div className="bg-[#111] border border-zinc-900 p-10 aspect-square flex items-center justify-center">
          <CustomImage
            src={product.url_imagem}
            alt={product.nome_produto}
            className=""
          />
        </div>

        <div className="flex flex-col gap-8">
          <div>
            <span className="text-(--color-primary) font-bold uppercase tracking-widest text-xs">
              {product.categoria_produto}
            </span>
            <div className="flex items-center justify-between gap-4 mt-2">
              <h1 className="text-4xl font-black text-white uppercase italic leading-tight">
                {product.nome_produto}
              </h1>

              <button
                onClick={() => setShowDeleteModal(true)}
                className="p-3 bg-zinc-900 border border-zinc-800 text-zinc-500 hover:text-red-500 hover:border-red-500 transition-all shrink-0"
                title="Deletar Produto"
              >
                <Trash2 size={24} />
              </button>
            </div>
            <div className="mt-6">
              <p className="text-zinc-400 text-sm">Preço no PIX</p>
              <span className="text-4xl font-black text-(--color-primary)">
                {new Intl.NumberFormat("pt-BR", {
                  style: "currency",
                  currency: "BRL",
                }).format(product.preco)}
              </span>
            </div>
          </div>

          <hr className="border-zinc-800" />

          <div className="grid grid-cols-2 gap-4">
            <h3 className="col-span-2 text-white font-bold uppercase text-sm italic">
              Especificações Técnicas
            </h3>
            <div className="bg-[#111] p-3 border border-zinc-900">
              <p className="text-zinc-500 text-[10px] uppercase">Peso</p>
              <p className="text-white font-mono">
                {product.medidas.peso_produto_gramas}g
              </p>
            </div>
            <div className="bg-[#111] p-3 border border-zinc-900">
              <p className="text-zinc-500 text-[10px] uppercase">
                Dimensões (CxAxL)
              </p>
              <p className="text-white font-mono">
                {product.medidas.comprimento_centimetros}x
                {product.medidas.altura_centimetros}x
                {product.medidas.largura_centimetros} cm
              </p>
            </div>
          </div>

          <div className="flex gap-8 mt-4">
            <div>
              <p className="text-zinc-500 text-[10px] uppercase font-bold">
                Total de Avaliações
              </p>
              <p className="text-white font-bold">
                {product.estatisticas.total_avaliacoes}
              </p>
            </div>
            <div>
              <p className="text-zinc-500 text-[10px] uppercase font-bold">
                Total Vendas
              </p>
              <p className="text-white font-bold">
                {product.estatisticas.total_vendas}
              </p>
            </div>
            <div>
              <p className="text-zinc-500 text-[10px] uppercase font-bold">
                Média Nota
              </p>
              <p className="text-(--color-primary) font-bold">
                ★ {product.estatisticas.media_nota}
              </p>
            </div>
          </div>

          <button className="w-full bg-(--color-primary) text-black font-black py-4 uppercase hover:bg-yellow-400 transition-colors mt-4">
            Adicionar ao Carrinho
          </button>

          <div className="container mx-auto px-4 mt-5 mb-20 md:col-span-2">
            <h3 className="text-2xl font-black text-white uppercase italic mb-8 border-l-4 border-(--color-primary) pl-4">
              Avaliações de Clientes
            </h3>

            {loadingReviews ? (
              <div className="flex items-center gap-3 text-zinc-500 animate-pulse">
                <div className="w-4 h-4 bg-(--color-primary) rounded-full animate-bounce" />
                <span className="text-sm font-bold uppercase italic">
                  Sincronizando avaliações...
                </span>
              </div>
            ) : reviews.length > 0 ? (
              <div className="grid grid-cols-1 gap-4">
                {reviews.map((rev) => (
                  <ReviewItem key={rev.id_avaliacao} review={rev} />
                ))}
              </div>
            ) : (
              <p className="text-zinc-600 italic">
                Nenhuma avaliação para este produto ainda.
              </p>
            )}
          </div>
        </div>
      </div>
    </MainLayout>
  );
};
