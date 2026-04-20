import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import { MainLayout } from "../components/templates/main-layout";
import { CustomInput } from "../components/atoms/custom-input";
import { CustomButton } from "../components/atoms/custom-button";
import { CATEGORIES_DATA } from "../models/categorias"

const api = axios.create({
  baseURL: "http://localhost:8000",
});


export const EditProductPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [fetching, setFetching] = useState(true);

  const [formData, setFormData] = useState({
    nome_produto: "",
    categoria_produto: "",
    peso_produto_gramas: 0,
    comprimento_centimetros: 0,
    altura_centimetros: 0,
    largura_centimetros: 0,
  });

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await api.get(`/produtos/${id}`);
        const product = response.data;

        setFormData({
          nome_produto: product.nome_produto,
          categoria_produto: product.categoria_produto,
          peso_produto_gramas: product.medidas?.peso_produto_gramas || 0,
          comprimento_centimetros:
            product.medidas?.comprimento_centimetros || 0,
          altura_centimetros: product.medidas?.altura_centimetros || 0,
          largura_centimetros: product.medidas?.largura_centimetros || 0,
        });
      } catch (err) {
        console.error("Erro ao carregar produto:", err);
        alert("Produto não encontrado.");
        navigate("/");
      } finally {
        setFetching(false);
      }
    };

    fetchProduct();
  }, [id, navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await api.patch(`/produtos/${id}`, {
        nome_produto: formData.nome_produto,
        categoria_produto: formData.categoria_produto,
        peso_produto_gramas: Number(formData.peso_produto_gramas),
        comprimento_centimetros: Number(formData.comprimento_centimetros),
        altura_centimetros: Number(formData.altura_centimetros),
        largura_centimetros: Number(formData.largura_centimetros),
      });

      alert("Produto atualizado com sucesso!");
      navigate("/");
    } catch (err) {
      console.error("Erro ao atualizar:", err);
      alert("Erro ao atualizar produto.");
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ) => {
    const { name, value } = e.target;

    if (name === "categoria_produto") {
      const category = CATEGORIES_DATA.find((cat) => cat.value === value);
      setFormData((prev) => ({
        ...prev,
        categoria_produto: value,
        url_imagem: category ? category.image : prev.url_imagem,
      }));
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }));
    }
  };

  if (fetching)
    return <div className="text-white p-10">Carregando dados...</div>;

  return (
    <MainLayout>
      <div className="container mx-auto px-4 py-12 max-w-2xl">
        <h1 className="text-4xl font-black text-white uppercase italic mb-8 border-l-4 border-(--color-primary) pl-4">
          Editar Produto
        </h1>

        <form
          onSubmit={handleSubmit}
          className="grid grid-cols-1 md:grid-cols-2 gap-6 bg-[#111] p-8 border border-zinc-900"
        >
          <div className="md:col-span-2">
            <label className="text-zinc-500 uppercase text-xs font-bold mb-2 block">
              Nome do Produto
            </label>
            <CustomInput
              name="nome_produto"
              value={formData.nome_produto}
              onChange={handleChange}
              required
            />
          </div>

          <div>
            <label className="text-zinc-500 uppercase text-xs font-bold mb-2 block">
              Categoria
            </label>
            <select
              name="categoria_produto"
              className="w-full bg-[#080808] border border-zinc-800 text-white p-3 focus:outline-none focus:border-(--color-primary) appearance-none"
              onChange={handleChange}
              value={formData.categoria_produto}
              required
            >
              {CATEGORIES_DATA.map((cat) => (
                <option key={cat.value} value={cat.value}>
                  {cat.label}
                </option>
              ))}
            </select>
          </div>

          <h3 className="md:col-span-2 text-white font-bold uppercase text-sm italic mt-4 border-b border-zinc-800 pb-2">
            Medidas e Peso
          </h3>

          <div>
            <label className="text-zinc-500 uppercase text-xs font-bold mb-2 block">
              Peso (g)
            </label>
            <CustomInput
              name="peso_produto_gramas"
              type="number"
              value={formData.peso_produto_gramas}
              onChange={handleChange}
              required
            />
          </div>

          <div>
            <label className="text-zinc-500 uppercase text-xs font-bold mb-2 block">
              Comp. (cm)
            </label>
            <CustomInput
              name="comprimento_centimetros"
              type="number"
              value={formData.comprimento_centimetros}
              onChange={handleChange}
              required
            />
          </div>

          <div>
            <label className="text-zinc-500 uppercase text-xs font-bold mb-2 block">
              Altura (cm)
            </label>
            <CustomInput
              name="altura_centimetros"
              type="number"
              value={formData.altura_centimetros}
              onChange={handleChange}
              required
            />
          </div>

          <div>
            <label className="text-zinc-500 uppercase text-xs font-bold mb-2 block">
              Largura (cm)
            </label>
            <CustomInput
              name="largura_centimetros"
              type="number"
              value={formData.largura_centimetros}
              onChange={handleChange}
              required
            />
          </div>

          <div className="md:col-span-2 mt-6 flex gap-4">
            <CustomButton
              type="button"
              variant="secondary"
              onClick={() => navigate("/")}
              className="flex-1"
            >
              CANCELAR
            </CustomButton>
            <CustomButton
              type="submit"
              variant="primary"
              className="flex-1"
              disabled={loading}
            >
              {loading ? "SALVANDO..." : "SALVAR ALTERAÇÕES"}
            </CustomButton>
          </div>
        </form>
      </div>
    </MainLayout>
  );
};
