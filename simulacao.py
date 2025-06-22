from vpython import *
import random
import time

def simular_efeito_hall(Tensao_sensor):

    # ========== Constantes físicas ==========
    q = -1.6e-19 # carga do elétron (C)
    m = 9.11e-31  # massa do elétron (Kg)
    v0 = vector(0, 0, 0)  # velocidade inicial no eixo x
    dt = 1e-11  # passo de tempo (pequeno para alta aceleração)
    i = 4.2e-3

    # ========== Parâmetros do sensor ==========

    # V (tensão lida no sensor)
    v_offset = 1.5            # V (tensão de referência do sensor)
    s = 1.8e-3         # V/Gauss
    w = 1e-3           # m (largura do condutor)
    d = 1e-5           # espessura
    sigma = 1e3        # condutividade do silício dopado (S/m)

    # ========== Dados coletados ==========
    # Campos iniciais
    Tensao_hall = Tensao_sensor - v_offset
    B_intensidade = ((Tensao_hall / s) * 1e-4)/100  # Gauss para Tesla

    # Campo elétrico gerador da corrente
    A = w * d
    J = i / A
    E_intensidade = J / sigma

    E = vector(-E_intensidade, 0, 0)
    B = vector(0, B_intensidade, 0)

    # ========== Visualização ==========
    scene = canvas(title="Efeito Hall com Campo Elétrico Dinâmico",
                width=800, height=600)

    # Condutor e placas
    bloco = box(pos=vector(0, 0, 0), size=vector(
        10e-3, 1e-3, 2e-3), color=color.gray(0.6), opacity=0.3)
    placa_esquerda = box(pos=vector(0, 0, -1e-3), size=vector(10e-3,
                        1e-3, 0.1e-3), color=color.blue, opacity=0.5)
    placa_direita = box(pos=vector(0, 0,  1e-3), size=vector(10e-3,
                        1e-3, 0.1e-3), color=color.red,  opacity=0.5)

    # Listas de elétrons
    eletrons_moveis = []
    eletrons_acumulados = []

    # Contadores de carga acumulada
    n_esquerda = 0
    n_direita = 0

    # ========== Criação de elétrons ==========

    def criar_eletron():
        e = sphere(
            pos=vector(-5e-3, 0, 0),
            radius=0.1e-5,
            color=color.cyan,
            make_trail=True
        )
        e.vel = v0
        eletrons_moveis.append(e)


    # ========== Estado dos campos ==========
    campo_eletrico_ativo = True
    campo_magnetico_ativo = True

    def toggle_campo_eletrico():
        global campo_eletrico_ativo
        campo_eletrico_ativo = not campo_eletrico_ativo
        botao_campo_eletrico.text = "Desligar Campo Elétrico" if campo_eletrico_ativo else "Ligar Campo Elétrico"

    def toggle_campo_magnetico():
        global campo_magnetico_ativo
        campo_magnetico_ativo = not campo_magnetico_ativo
        botao_campo_magnetico.text = "Desligar Campo Magnético" if campo_magnetico_ativo else "Ligar Campo Magnético"

    # Botões
    botao_campo_eletrico = button(
        text="Desligar Campo Elétrico", bind=lambda _: toggle_campo_eletrico())
    botao_campo_magnetico = button(
        text="Desligar Campo Magnético", bind=lambda _: toggle_campo_magnetico())

    # ========== Loop de simulação ==========
    tempo_inicial = time.time()
    intervalo_geracao = 0.5  # segundos

    while True:
        rate(500)

        # Geração periódica de elétrons
        if time.time() - tempo_inicial > intervalo_geracao:
            criar_eletron()
            tempo_inicial = time.time()

        # Atualiza movimento
        for e in eletrons_moveis[:]:
            # Força elétrica (externa)
            F_elet = q * E if campo_eletrico_ativo else vector(0, 0, 0)

            # Força magnética
            F_mag = q * cross(e.vel, B) if campo_magnetico_ativo  else vector(0, 0, 0)
                
            # Campo Hall dinâmico
            delta_n = n_direita - n_esquerda
            # Campo Hall real (a partir do acúmulo de carga)
            L = 5e-3  # comprimento lateral (x)
            A_face = L * w   # área da face onde há acúmulo
            sigma_s = (abs(q) * 1e3 * delta_n) / A_face  # densidade por área
            epsilon_0 = 8.85e-12  # permissividade do vácuo
            E_hall = vector(0, 0, sigma_s / epsilon_0)

            # Força de Hall efetiva
            F_elet_hall = q * E_hall

            # Movimento
            a = (F_elet + F_mag + F_elet_hall) / m
            e.vel += a * dt
            e.pos += e.vel * dt

            if e.pos.z < -bloco.size.z / 2:
                n_esquerda += 1
                eletrons_acumulados.append(e)
                eletrons_moveis.remove(e)
                e.visible = False
            elif e.pos.z > bloco.size.z / 2:
                n_direita += 1
                eletrons_acumulados.append(e)
                eletrons_moveis.remove(e)
                e.visible = False

            # Fora da área do bloco (em x ou y)
            if abs(e.pos.x) > bloco.size.x / 2 or abs(e.pos.y) > bloco.size.y / 2:
                eletrons_moveis.remove(e)
                e.visible = False

