from vpython import *

# Constantes físicas
q = -1.6e-19  # carga do elétron
m = 9.11e-31  # massa do elétron
v0 = vector(0, 0, 0)  # velocidade inicial (x)
dt = 5e-3  # passo de tempo

# Parâmetros iniciais dos campos
E_magnitude = -1e-12
B_magnitude = 1e-12

# Visual
scene = canvas(title="Efeito Hall")
bloco = box(pos=vector(0, 0, 0), size=vector(
    4, 0.5, 1), color=color.gray(0.6), opacity=0.3)

# Elétron
e = sphere(pos=vector(-1.5, 0, 0), radius=0.05,
           color=color.cyan, make_trail=True)
v = v0

# Valores dos campos (iniciais)
E = vector(E_magnitude, 0, 0)
B = vector(0, B_magnitude, 0)

# Propriedades do meio
eta = 1e-30  # viscosidade dinâmica do meio (ex: água ~1e-3 Pa.s)
raio = 5e-2  # raio da partícula (mesmo que o raio do sphere)
gama = 6 * pi * eta * raio  # coeficiente de resistência de Stokes

# Estado dos campos
campo_eletrico_ativo = True
campo_magnetico_ativo = True

# Funções dos botões


def toggle_campo_eletrico():
    global campo_eletrico_ativo
    campo_eletrico_ativo = not campo_eletrico_ativo
    botao_campo_eletrico.text = "Desligar Campo Elétrico" if campo_eletrico_ativo else "Ligar Campo Elétrico"


def toggle_campo_magnetico():
    global campo_magnetico_ativo
    campo_magnetico_ativo = not campo_magnetico_ativo
    botao_campo_magnetico.text = "Desligar Campo Magnético" if campo_magnetico_ativo else "Ligar Campo Magnético"


# Interface: botões
botao_campo_eletrico = button(
    text="Desligar Campo Elétrico", bind=lambda _: toggle_campo_eletrico())
botao_campo_magnetico = button(
    text="Desligar Campo Magnético", bind=lambda _: toggle_campo_magnetico())


# Loop de simulação
while True:
    rate(300)

    e.pos += v * dt

    # Forças
    F_elet = q * E if campo_eletrico_ativo else vector(0, 0, 0)
    F_mag = q * cross(v, B) if campo_magnetico_ativo else vector(0, 0, 0)
    F_res = -gama * v

    F_tot = F_elet + F_mag + F_res
    a = F_tot / m
    v += a * dt

    # Condição de reinício: se sair dos limites da caixa
    if abs(e.pos.x) > bloco.size.x/2 or abs(e.pos.y) > bloco.size.y/2 or abs(e.pos.z) > bloco.size.z/2:
        e.pos = vector(-1.5, 0, 0)  # reposiciona
        v = v0                     # reseta velocidade
        e.clear_trail()             # limpa o rastro
