import random
from app.model.jogador import Jogador
from app.model.propriedade import Propriedade


class Tabuleiro:
    def __init__(self):
        self.__jogadores = []
        self.__propriedades = []

    @property
    def jogadores(self):
        return self.__jogadores

    @property
    def propriedades(self):
        return self.__propriedades

    @jogadores.setter
    def jogadores(self, jogadores: list):
        if not isinstance(jogadores, list):
            raise TypeError

        self.__jogadores = jogadores

    @propriedades.setter
    def propriedades(self, propriedades: list):
        if not isinstance(propriedades, list):
            raise TypeError

        if len(propriedades) != 20:
            raise Exception(
                "Número inválido de propriedades. Necessário informar vinte propriedades para iniciar o jogo."
            )

        self.__propriedades = propriedades

    def adicionar_jogador(self, jogador: Jogador):
        if not isinstance(jogador, Jogador):
            raise TypeError

        self.__jogadores.append(jogador)

    def adicionar_propriedade(self, propriedade: Propriedade):
        if not isinstance(propriedade, Propriedade):
            raise TypeError

        if len(self.__propriedades) >= 20:
            print("Número máximo de vinte propriedades atingido. A propriedade {} não será adicionada".format(
                propriedade.nome
            ))

        self.__propriedades.append(propriedade)

    def definir_ordem_jogadas(self):
        random.shuffle(self.__jogadores)
