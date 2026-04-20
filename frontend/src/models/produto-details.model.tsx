import type { ProductCardModel } from "./produto-card.model";

export interface ProductDetailsModel extends ProductCardModel {
  medidas: {
    peso_produto_gramas: number;
    comprimento_centimetros: number;
    altura_centimetros: number;
    largura_centimetros: number;
  };
  estatisticas: {
    total_vendas: number;
    total_avaliacoes: number;
    media_nota: number;
  };
}
