import random
from abc import ABC, abstractmethod


class Jogador(ABC):
    def __init__(self, nome, saldo_inicial=300.00):
        if not isinstance(nome, str) or not isinstance(saldo_inicial, float):
            raise TypeError

        self.__nome = nome
        self.__saldo_inicial = saldo_inicial
        self.__saldo = saldo_inicial
        self.__jogando = True
        self.__posicao_tabuleiro = 0

    @property
    def nome(self):
        return self.__nome

    @property
    def saldo_inicial(self):
        return self.__saldo_inicial

    @property
    def saldo(self):
        return self.__saldo

    @property
    def jogando(self):
        return self.__jogando

    @jogando.setter
    def jogando(self, jogando: bool):
        if not isinstance(jogando, bool):
            raise TypeError

        self.__jogando = jogando

    @property
    def posicao_tabuleiro(self):
        return self.__posicao_tabuleiro

    @posicao_tabuleiro.setter
    def posicao_tabuleiro(self, posicao_tabuleiro: int):
        if not isinstance(posicao_tabuleiro, int):
            raise TypeError

        self.__posicao_tabuleiro = 0 if posicao_tabuleiro < 0 else posicao_tabuleiro

    def valor_disponivel_saque(self, valor: float) -> bool:
        if not isinstance(valor, float):
            raise TypeError

        return True if self.__saldo >= valor else False

    def saque(self, valor: float, zerar_saldo: bool = False) -> bool:
        if not isinstance(valor, float):
            raise TypeError

        if valor < 0:
            raise Exception("Valor de saque inválido")

        if not self.valor_disponivel_saque(valor) and not zerar_saldo:
            # print(
            #     """
            #     Valor de R$ {} indisponível para saque pelo jogador {}.
            #     Saldo atual: R$ {}.
            #     """.format(valor, self.__nome, self.__saldo)
            # )

            return False

        self.__saldo -= valor

        if self.__saldo < 0 and zerar_saldo:
            self.__saldo = 0

        if self.__saldo == 0:
            self.__jogando = False

        return True

    def deposito(self, valor: float) -> bool:
        if not isinstance(valor, float):
            raise TypeError

        if valor < 0:
            raise Exception("Valor de depósito inválido")

        self.__saldo += valor

        return True

    def realizar_jogada(self):
        rolagem_dado = random.choice(range(1, 7))

        self.__posicao_tabuleiro += rolagem_dado

        if self.__posicao_tabuleiro > 19:
            self.__saldo += 100.00

            # print(
            #     """
            #     O jogador {} completou uma volta no tabuleiro e por isso recebeu R$ 100,00 de saldo.
            #     Saldo: R$ {}.
            #     """.format(self.__nome, self.__saldo)
            # )

            self.__posicao_tabuleiro -= 19

    @abstractmethod
    def analisar_oportunidade_compra(self, propriedade) -> bool:
        pass
