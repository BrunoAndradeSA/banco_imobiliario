from app.model.jogador import Jogador
from app.model.propriedade import Propriedade


class JogadorCauteloso(Jogador):
    def analisar_oportunidade_compra(self, propriedade: Propriedade) -> bool:
        if self.valor_disponivel_saque(propriedade.valor_compra) and (self.saldo - propriedade.valor_compra) >= 80:
            return propriedade.comprar(self)
        else:
            return False
