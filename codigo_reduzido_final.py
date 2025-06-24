
#fazendo a importação das bibliotecas necessárias
import serial #biblioteca para conexão com arduíno
import time #biblioteca para estabelecer uma pausa para os comandos do arduíno
from vpython import * #biblioteca para a simulação e para a plotagem de gráfico

#inicializando comunicação com arduíno
arduino = serial.Serial('COM3', 9600)
time.sleep(2)

#função de medir e receber os dados com o arduíno
def receber_dados_arduino():

    dados_tensao = {}
    campos_por_distancia = {}
    distancias = [1, 2, 3, 4, 5]
    corrente = 4.2e-3
    sensitividade = 1.8
    numero_medida = 1

    while numero_medida < 6 :
        frase = 'Coloque o imã na marcação ' + str(numero_medida)+ '. Escreva "' + str(numero_medida) +'" quando estiver pronto para começar a fazer a medida nº '+ str(numero_medida) + ' do imã, a '+ str(numero_medida) +'cm de distância'
        medida = input(frase)
        if medida == str(numero_medida):
            arduino.write(b'Medir')
            time.sleep(0.1)
            tensaohall = float(arduino.readline().decode().strip()) - 2.5
            print("Valor medido- Tensão Hall:", tensaohall)
            quer_repetir = str.lower(input('Digite "Repetir" caso queira repetir, ou qualquer outro caractere para continuar.'))
            if quer_repetir == "repetir":
                medida = ""
                tensaohall = 0
            else:
                dados_tensao[numero_medida] = [float(tensaohall)]
                campos_por_distancia[numero_medida] = [float(tensaohall)/(corrente*sensitividade)]
                numero_medida = numero_medida + 1
                tensaohall = 0

    arduino.close()

    print("Valores medidos! Aguarde para a confecção do gráfico:")           
    return distancias, campos_por_distancia, dados_tensao

#função para receber os dados teóricos do usuário
def receber_dados_usuario():
    """
    Recebe distâncias e corrente do usuário,
    calcula campo magnético e tensão Hall teoricamente,
    retorna dados organizados para plotagem.
    """
    n = int(input("Quantos pontos de distância você quer analisar? "))
    distancias = []
    for i in range(n):
        d = float(input(f"Digite a distância {i+1} (em cm): "))
        distancias.append(d)
 
    corrente = 4.2e-3
 
    # Constantes ajustadas para simulação didática
    corrente = 4.2e-3
    n_portadores = 1e22   # densidade de portadores (semicondutor)
    q = 1.6e-19           # carga do elétron (C)
    t = 1e-4              # espessura do sensor (m)
    k = 0.0035            # constante para cálculo do campo magnético (ajustada para cm)
 
    campos_por_distancia = {}
    dados_tensao = {}
 
    for d in distancias:
        campo = k / (d**3)  # campo magnético em Tesla
        tensao = (campo * corrente) / (n_portadores * q * t)  # tensão Hall em Volts
        campos_por_distancia[d] = [campo]
        dados_tensao[d] = [tensao]
        print(f"Distância: {d} cm | Campo: {campo:.6f} T | Tensão Hall: {tensao:.6f} V")
 
    return distancias, campos_por_distancia, dados_tensao
 

#função para plotar os gráficos
def plotar_graficos(distancias, campos_por_distancia, dados_tensao):

    from vpython import graph, gcurve, color
    """
    Plota dois gráficos:
   
    2) Tensão Hall x Distância
    """
 
    graf2 = graph(title="Tensão Hall x Distância", xtitle="Distância (cm)", ytitle="Tensão Hall (V)", width=600, height=400)
    curva2 = gcurve(color=color.blue, label="Dados")
    for d in distancias:
        tensao = dados_tensao[d][0] if dados_tensao[d] else 0
        curva2.plot(d, tensao)

#função da simulação
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
 
#bloco de ações
if __name__ == "__main__":
    print("H.E.L.L.O., world!")
    print("Bem vindo ao Hall Effect Lab for Learning and Observation! Você deseja usar valor teóricos ou valores obtidos através de um arduíno?")
    modo = input("Digite '1' para inserir dados manualmente ou '2' para coletar do Arduino: ")

    if modo == '1':
        distancias, campos_por_distancia, dados_tensao= receber_dados_usuario()
    elif modo == '2':
        distancias, campos_por_distancia, dados_tensao = receber_dados_arduino()
        if distancias is None:
            
            print("Falha na leitura do Arduino. Encerrando.")
            exit()
    else:
        print("Opção inválida. Encerrando.")
        exit()

    print("Gerando gráficos...")
    plotar_graficos(distancias, campos_por_distancia, dados_tensao)
    print("Olhe o que acontece por dentro do efeito Hall! Qual ponto você deseja ver?")
    dist_simu = int(input("Digite o número, em cm, do ponto que você quer ver."))
    simular_efeito_hall(dados_tensao[dist_simu][0])
    input("Pressione Enter para sair e fechar os gráficos...")
