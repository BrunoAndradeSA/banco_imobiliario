from app.model.jogador import Jogador


class Propriedade:
    def __init__(self, nome, proprietario, valor_compra, valor_aluguel):
        if not isinstance(nome, str) or \
           (not isinstance(proprietario, Jogador) and proprietario) or \
           not isinstance(valor_compra, float) or \
           not isinstance(valor_aluguel, float):
            raise TypeError

        self.__nome = nome
        self.__proprietario = proprietario
        self.__valor_compra = valor_compra
        self.__valor_aluguel = valor_aluguel

    @property
    def nome(self):
        return self.__nome

    @property
    def proprietario(self):
        return self.__proprietario

    @property
    def valor_compra(self):
        return self.__valor_compra

    @property
    def valor_aluguel(self):
        return self.__valor_aluguel

    def disponivel_compra(self) -> bool:
        return True if not self.__proprietario else False

    def comprar(self, comprador: Jogador) -> bool:
        if not isinstance(comprador, Jogador):
            raise TypeError

        if self.__proprietario == comprador:
            return True

        if not self.disponivel_compra:
            # print(
            #     """
            #     A proprieidade {} não está disponível para compra pois já pertence ao jogador {}.
            #     """.format(self.__nome, self.__proprietario.nome)
            # )

            return False

        if not comprador.valor_disponivel_saque(self.__valor_compra):
            # print(
            #     """
            #     Jogador {} não possui saldo suficiente para comprar a propriedade {} no valor de R$ {}.
            #     Saldo do {}: R$ {}
            #     """.format(
            #         comprador.nome,
            #         self.__nome,
            #         self.__valor_compra,
            #         comprador.nome,
            #         comprador.saldo
            #     )
            # )

            return False

        comprador.saque(self.__valor_compra)
        self.__proprietario = comprador

        return True

    def verificar_aluguel(self, jogador: Jogador) -> bool:
        if not isinstance(jogador, Jogador):
            raise TypeError

        if not self.disponivel_compra() and self.__proprietario != jogador:
            jogador.saque(self.__valor_aluguel, True)
            self.__proprietario.deposito(self.__valor_aluguel)

            # print(
            #     """
            #     O jogador {} recebeu R$ {} de aluguél do jogador {} pela propriedade {}.
            #     """.format(
            #         self.__proprietario.nome,
            #         self.__valor_aluguel,
            #         jogador.nome,
            #         self.__nome
            #     )
            # )

            return True

    def desocupar(self):
        self.__proprietario = None
