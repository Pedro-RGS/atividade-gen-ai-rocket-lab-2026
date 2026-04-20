import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { MainLayout } from "../components/templates/main-layout";
import { CustomInput } from "../components/atoms/custom-input";
import { CustomButton } from "../components/atoms/custom-button";
import { CATEGORIES_DATA } from "../models/categorias"

const api = axios.create({
  baseURL: "http://localhost:8000",
});

export const CreateProductPage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    nome_produto: "",
    categoria_produto: "",
    preco: 0,
    url_imagem: "",
    peso_produto_gramas: 0,
    comprimento_centimetros: 0,
    altura_centimetros: 0,
    largura_centimetros: 0,
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.categoria_produto) {
      alert("Por favor, selecione uma categoria.");
      return;
    }

    setLoading(true);

    try {
      await api.post("/produtos", {
        nome_produto: formData.nome_produto,
        categoria_produto: formData.categoria_produto,
        preco: Number(formData.preco),
        url_imagem: formData.url_imagem,
        peso_produto_gramas: Number(formData.peso_produto_gramas),
        comprimento_centimetros: Number(formData.comprimento_centimetros),
        altura_centimetros: Number(formData.altura_centimetros),
        largura_centimetros: Number(formData.largura_centimetros),
      });

      alert("Produto criado com sucesso!");
      navigate("/");
    } catch (err) {
      console.error("Erro ao criar produto:", err);
      alert("Erro ao criar produto. Verifique os dados.");
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
        url_imagem: category ? category.image : "",
      }));
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }));
    }
  };

  return (
    <MainLayout>
      <div className="container mx-auto px-4 py-12 max-w-2xl">
        <h1 className="text-4xl font-black text-white uppercase italic mb-8 border-l-4 border-(--color-primary) pl-4">
          Cadastrar Novo Produto
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
              placeholder="Ex: Teclado gamer"
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
              required
              value={formData.categoria_produto}
            >
              <option value="" disabled>
                Selecione uma opção
              </option>
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
              Peso (Gramas)
            </label>
            <CustomInput
              name="peso_produto_gramas"
              type="number"
              onChange={handleChange}
              required
            />
          </div>

          <div>
            <label className="text-zinc-500 uppercase text-xs font-bold mb-2 block">
              Comprimento (cm)
            </label>
            <CustomInput
              name="comprimento_centimetros"
              type="number"
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
              onChange={handleChange}
              required
            />
          </div>

          <div className="md:col-span-2 mt-6">
            <CustomButton
              type="submit"
              variant="primary"
              className="w-full py-4 text-lg"
              disabled={loading}
            >
              {loading ? "PROCESSANDO..." : "FINALIZAR CADASTRO"}
            </CustomButton>
          </div>
        </form>
      </div>
    </MainLayout>
  );
};
