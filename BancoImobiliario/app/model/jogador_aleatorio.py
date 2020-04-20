import random
from app.model.jogador import Jogador
from app.model.propriedade import Propriedade


class JogadorAleatorio(Jogador):
    def analisar_oportunidade_compra(self, propriedade: Propriedade) -> bool:
        if self.valor_disponivel_saque(propriedade.valor_compra) and random.choice([True, False]):
            return propriedade.comprar(self)
        else:
            return False
