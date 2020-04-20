from app.model.jogador import Jogador
from app.model.propriedade import Propriedade


class JogadorExigente(Jogador):
    def analisar_oportunidade_compra(self, propriedade: Propriedade) -> bool:
        if self.valor_disponivel_saque(propriedade.valor_compra) and propriedade.valor_aluguel > 50:
            return propriedade.comprar(self)
        else:
            return False
