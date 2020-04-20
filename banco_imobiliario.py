# coding: windows-1252
import random
from abc import ABC, abstractmethod


##############################################################################
#
# DEFINIÇÃO DE CLASSES DE MODELO - Jogador
#
##############################################################################
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


##############################################################################
#
# DEFINIÇÃO DE CLASSES DE MODELO - Propriedade
#
##############################################################################
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


##############################################################################
#
# DEFINIÇÃO DE CLASSES DE MODELO - Tabuleiro
#
##############################################################################
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


##############################################################################
#
# ESPECIALIZAÇÃO DE COMPORTAMENTO - Jogador do tipo Impulsivo
#
##############################################################################
class JogadorImpulsivo(Jogador):
    def analisar_oportunidade_compra(self, propriedade: Propriedade) -> bool:
        return propriedade.comprar(self)


##############################################################################
#
# ESPECIALIZAÇÃO DE COMPORTAMENTO - Jogador do tipo Exigente
#
##############################################################################
class JogadorExigente(Jogador):
    def analisar_oportunidade_compra(self, propriedade: Propriedade) -> bool:
        if propriedade.valor_aluguel > 50:
            return propriedade.comprar(self)
        else:
            return False


##############################################################################
#
# ESPECIALIZAÇÃO DE COMPORTAMENTO - Jogador do tipo Cauteloso
#
##############################################################################
class JogadorCauteloso(Jogador):
    def analisar_oportunidade_compra(self, propriedade: Propriedade) -> bool:
        if (self.saldo - propriedade.valor_compra) >= 80:
            return propriedade.comprar(self)
        else:
            return False


##############################################################################
#
# ESPECIALIZAÇÃO DE COMPORTAMENTO - Jogador do tipo Aleatório
#
##############################################################################
class JogadorAleatorio(Jogador):
    def analisar_oportunidade_compra(self, propriedade: Propriedade) -> bool:
        if random.choice([True, False]):
            return propriedade.comprar(self)
        else:
            return False


##############################################################################
#
# DEFINIÇÃO DOS MÉTODOS
#
##############################################################################
comportamentos = ['IMPULSIVO', 'EXIGENTE', 'CAUTELOSO', 'ALEATÓRIO']
vitorias = [0, 0, 0, 0]


def contabilizar_vitorias(jogador: Jogador):
    if not isinstance(jogador, Jogador):
        raise TypeError

    if isinstance(jogador, JogadorImpulsivo):
        vitorias[0] += 1
    elif isinstance(jogador, JogadorExigente):
        vitorias[1] += 1
    elif isinstance(jogador, JogadorCauteloso):
        vitorias[2] += 1
    else:
        vitorias[3] += 1


def inicializar_jogadores() -> list:
    jogadores = []

    jogador_impulsivo = JogadorImpulsivo('JOGADOR IMPULSIVO')
    jogador_exigente = JogadorExigente('JOGADOR EXIGENTE')
    jogador_cauteloso = JogadorCauteloso('JOGADOR CAUTELOSO')
    jogador_aleatorio = JogadorAleatorio('JOGADOR ALEATÓRIO')

    jogadores.append(jogador_impulsivo)
    jogadores.append(jogador_exigente)
    jogadores.append(jogador_cauteloso)
    jogadores.append(jogador_aleatorio)

    return jogadores


def inicializar_propriedades() -> list:
    propriedades = []

    for i in range(20):
        valor_compra = float(random.choice(range(100, 300)))

        valor_aluguel = float(random.choice(range(10, 90)))

        propriedades.append(
            Propriedade(
                'PROPRIEDADE ' + str(i + 1),
                None,
                valor_compra,
                valor_aluguel
            )
        )

    return propriedades


##############################################################################
#
# MÉTODO DE INICIALIZAÇÃO DAS SIMULAÇÕES
#
##############################################################################
def iniciar_jogo():
    rodadas_corridas = 0

    vitorias_comportamentos = {}

    qtde_jogos_timeout = 0

    print(
        """
        ------------------------------------------------------------------------------------------------
        | INICIO DAS SIMULAÇÕES - [300 SIMULAÇÕES]                                                     |
        ------------------------------------------------------------------------------------------------
        """
    )

    for simulacao in range(300):
        tabuleiro = Tabuleiro()

        tabuleiro.jogadores = inicializar_jogadores()
        tabuleiro.propriedades = inicializar_propriedades()

        # for jogador in tabuleiro.jogadores:
        #     print(
        #         '| Jogador {} entrou no jogo com um saldo inicial de R$ {}.'.format(
        #             jogador.nome, jogador.saldo_inicial
        #         )
        #     )

        # print(
        #     """
        #     ------------------------------------------------------------------------------------------------
        #     """
        # )

        # for propriedade in tabuleiro.propriedades:
        #     print(
        #         '| Propriedade {} adicionada ao jogo. Compra: R$ {} | Aluguél: R$ {}.'.format(
        #             propriedade.nome, propriedade.valor_compra, propriedade.valor_aluguel
        #         )
        #     )

        nro_simulacao = simulacao + 1
        nro_rodada = 0
        vencedor = None

        tabuleiro.definir_ordem_jogadas()

        print(
            """
            ------------------------------------------------------------------------------------------------
            | SIMULAÇÃO NRO: {} - INICIO                                                                   |
            ------------------------------------------------------------------------------------------------
            """.format(nro_simulacao)
        )

        print(
            """
            ------------------------------------------------------------------------------------------------
            | ORDEM DE INICIO DOS JOGADORES                                                                 |
            ------------------------------------------------------------------------------------------------
            """
        )

        for jogador in tabuleiro.jogadores:
            print(
                """
                    -> {}
                """.format(jogador.nome)
            )

        for rodada in range(1000):
            nro_rodada = rodada + 1

            for jogador in tabuleiro.jogadores:
                jogador.realizar_jogada()

                propriedade = tabuleiro.propriedades[jogador.posicao_tabuleiro]

                propriedade.verificar_aluguel(jogador)

                jogador.analisar_oportunidade_compra(propriedade)

                if not jogador.jogando:
                    for propriedade in tabuleiro.propriedades:
                        if propriedade.proprietario == jogador:
                            propriedade.desocupar()

            jogadores_ativos = [j for j in tabuleiro.jogadores if j.jogando]

            if len(jogadores_ativos) == 1:
                vencedor = jogadores_ativos[0]

                rodadas_corridas += nro_rodada

                break

        if vencedor:
            print(
                """
                ************************************************************************************************
                *                                                                                              *
                * TEMOS UM VENCEDOR!                                                                           *
                *                                                                                              *
                ************************************************************************************************
                *
                *  O jogador {} venceu a simulação nro. {} na rodada de nro. {}, 
                *  com o saldo de R$ {}.
                *
                ************************************************************************************************
                """.format(
                    vencedor.nome,
                    nro_simulacao,
                    nro_rodada,
                    vencedor.saldo
                )
            )

            contabilizar_vitorias(vencedor)
        else:
            rodadas_corridas += 1000

            qtde_jogos_timeout += 1

            print(
                """
                ################################################################################################
                # FIM DE JOGO POR TIME OUT!                                                                    #
                ################################################################################################
                #
                #  O jogo da simulação nro. {} foi encerrado após a rodada de nro. {}.
                #
                ################################################################################################
                # RANKING DE JOGADORES DA SIMULAÇÃO NRO. {}                                                    #
                ################################################################################################
                """.format(
                    nro_simulacao,
                    nro_rodada,
                    nro_simulacao
                )
            )

            ranking_jogadores = sorted(
                tabuleiro.jogadores, 
                key=lambda x: [x.saldo, tabuleiro.jogadores.index(x)], 
                reverse=True
            )

            for jogador in ranking_jogadores:
                label_vencedor = ''

                if ranking_jogadores.index(jogador) == 0:
                    label_vencedor = '*** VENCEDOR ***'

                    contabilizar_vitorias(jogador)

                print(
                    """
                          #  -> {}º Lugar: {} com um saldo final de R$ {} {}
                    """.format(
                        ranking_jogadores.index(jogador) + 1,
                        jogador.nome,
                        jogador.saldo,
                        label_vencedor
                    )
                )

            print(
                """
                ################################################################################################
                """
            )

        print(
            """
            ------------------------------------------------------------------------------------------------
            | SIMULAÇÃO NRO: {} - FIM                                                                      |
            ------------------------------------------------------------------------------------------------
            """.format(nro_simulacao)
        )

    print(
        """
        ------------------------------------------------------------------------------------------------
        | FIM DAS SIMULAÇÕES - [300 SIMULAÇÕES]                                                        |
        ------------------------------------------------------------------------------------------------
        """
    )

    for k, v in zip(comportamentos, vitorias):
        vitorias_comportamentos.update({
            k: v
        })

    media_rodadas_partida = round(rodadas_corridas / 300, 2)

    percentual_vitoria_impulsivo = round((vitorias_comportamentos.get('IMPULSIVO') / 300) * 100, 2)
    percentual_vitoria_exigente = round((vitorias_comportamentos.get('EXIGENTE') / 300) * 100, 2)
    percentual_vitoria_cauteloso = round((vitorias_comportamentos.get('CAUTELOSO') / 300) * 100, 2)
    percentual_vitoria_aleatorio = round((vitorias_comportamentos.get('ALEATÓRIO') / 300) * 100, 2)

    print(
        """
        $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        $ ESTÁTISTICAS APÓS 300 SIMULAÇÕES                                                             $
        $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        $ -> Número de partidas finalizadas em timeout: {}
        $ -> Média de turnos por partida: {}
        $ -> Porcentagem de vitórias por comportamento do jogador:
        $   -> Impulsivo: {} %
        $   -> Exigente: {} %
        $   -> Cauteloso: {} %
        $   -> Aleatório: {} %
        $ -> Comportamento mais vencedor: {}
        $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        """.format(
            qtde_jogos_timeout,
            media_rodadas_partida,
            percentual_vitoria_impulsivo,
            percentual_vitoria_exigente,
            percentual_vitoria_cauteloso,
            percentual_vitoria_aleatorio,
            sorted(vitorias_comportamentos.items(), key=lambda x: x[1], reverse=True)[0][0]
        )
    )


if __name__ == '__main__':
    iniciar_jogo()
