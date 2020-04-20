import random
from app.model.jogador_impulsivo import JogadorImpulsivo
from app.model.jogador_exigente import JogadorExigente
from app.model.jogador_cauteloso import JogadorCauteloso
from app.model.jogador_aleatorio import JogadorAleatorio
from app.model.tabuleiro import Tabuleiro
from app.model.jogador import Jogador
from app.model.propriedade import Propriedade

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
            | ORDEM DE INICIO DOS JOGADORE                                                                 |
            ------------------------------------------------------------------------------------------------
            """.format(nro_simulacao)
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


def main():
    print(
        """
        ------------------------------------------------------------------------------------------------
        | INICIO DO JOGO                                                                               |
        ------------------------------------------------------------------------------------------------
        """
    )

    iniciar_jogo()

    print(
        """
        ------------------------------------------------------------------------------------------------
        | FIM DO JOGO                                                                                  |
        ------------------------------------------------------------------------------------------------
        """
    )
