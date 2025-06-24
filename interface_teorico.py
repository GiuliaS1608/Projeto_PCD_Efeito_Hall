Web VPython 3.2

####################################### Cena #######################################

scene = canvas(title="H.E.L.L.O World! <br>Efeito Hall com Campo Elétrico Dinâmico",
        width=800, height=500, align="right")
esp_l = wtext(text="<br>", align="left")
modo_livre = button(bind=mestre_livre, text="Simulação Livre", disabled=False)

# ========== Constantes físicas ==========
q = -1.6e-19          # carga do elétron (C)
m = 9.11e-31          # massa do elétron (Kg)
v0 = vector(0, 0, 0)  # velocidade inicial no eixo x
dt = 2e-11            # passo de tempo (pequeno para alta aceleração)
i = 4.2e-3            # intensidade da corrente (A)

# ========== Parâmetros do sensor ==========
s = 1.8e-3            # V/Gauss
w = 1e-3              # m (largura do condutor)
L = 5e-3              # comprimento lateral (x)
t = 1e-4              # espessura
sigma = 1e3           # condutividade do silício dopado (S/m)
n_portadores = 1e22   # densidade de portadores (semicondutor silício dopado)

###################################### Chaves ######################################

### Gráfico Livre
inicializacao_livre = False
key_grafico_livre = False
ha_grafico_livre = False

### Simulação Geral
escopo_simulacao = False
key_simulacao = False
ha_objetos = False

################################ Funções Internas ##################################

# Criação de Elétrons
def criar_eletron():
    e = sphere(pos=vector(-5e-3, 0, 0), radius=0.1e-5, 
        color=color.cyan, make_trail=True)
    e.vel = v0
    eletrons_moveis.append(e)

# Coleta das informações necessárias para a plotagem do gráfico
def dados_usuario(n, campo_magnetico_maximo, i, n_portadores, q, t):
    distancias = list(range(1, n + 1))
     
    """
    Para dipolos magnéticos tais que a distância é muito maior que qualquer dimensão de sua face aparente:
    B(d) = (μ0/4π) * (μ/d**3), 
    em que μ0 é a permeabilidade magnética no vácuo e μ é o momento dipolar.
    Consideremos o campo magnético máximo com d = 0,01 m, isto é, um valor x T.cm³.
    """
    
    campos_por_distancia = {}
    dados_tensao = {}
 
    for d in distancias:
        B_intensidade = campo_magnetico_maximo / (d**3)  # campo magnético em Tesla
        tensao = (B_intensidade * i) / (n_portadores * -q * t)  # tensão Hall em Volts
        campos_por_distancia[d] = [B_intensidade]
        dados_tensao[d] = [tensao]
 
    return distancias, campos_por_distancia, dados_tensao

# Plotagem do gráfico Tensão Hall (V) x Distância (cm)
def plotar_graficos(distancias, campos_por_distancia, dados_tensao, campo_magnetico_maximo):
    global graf2
    graf2 = graph(title=f"Tensão Hall x Distância a {campo_magnetico_maximo}T máx.",
            xtitle="Distância (cm)", ytitle="Tensão Hall (V)", width=400, height=300)
    curva2 = gcurve(color=color.blue, label="Dados")
    for d in distancias:
        tensao = dados_tensao[d][0] if dados_tensao[d] else 0
        curva2.plot(d, tensao)

############################ Funções dos Botões ############################        
    
### Modo Livre
def mestre_livre():
    global inicializacao_livre, campo_eletrico_ativo, campo_magnetico_ativo, ha_grafico_livre
    modo_livre.disabled = True
    
    if ha_grafico_livre == True:
        global key_simulacao, ha_objetos, B_intensidade, distancia_livre, distancia_maxima, campo_magnetico_maximo, graf2
        distancia_maxima = 0
        campo_magnetico_maximo = 0
        B_intensidade = 0
        distancia_livre = 1
        ha_grafico_livre = False
        key_simulacao = False
        opt_campo_eletrico.delete()
        opt_campo_magnetico.delete()
        iniciar_livre.delete()
        resetar_livre.delete()
        wt_slider.delete()
        slider_grafico_livre.delete()
        graf2.delete()
        esp_l1.delete()
        esp_l3.delete()
        esp_l4.delete()
        if ha_objetos == True:
            for obj in scene.objects:
                obj.visible = False
            del bloco
            del placa_direita
            del placa_esquerda
            eletrons_moveis = []
            eletrons_acumulados = []
        scene.forward = vector(0, 0, -1)
        scene.up = vector(0, 1, 0)
        
    inicializacao_livre = True
    campo_eletrico_ativo = True
    campo_magnetico_ativo = False
    
def define_campo_magnetico_maximo(evt):
    global campo_magnetico_maximo
    
    if evt.index < 1:
            pass
    elif evt.index == 1:
        campo_magnetico_maximo = 0.005
    elif evt.index == 2:
        campo_magnetico_maximo = 1
    elif evt.index == 3:
        campo_magnetico_maximo = 14

distancia_maxima = 0
def recebe_distancia_maxima(evt):
    global distancia_maxima, key_grafico_livre
    try:
        distancia_maxima = int(evt.text)
        if distancia_maxima > 1:
            key_grafico_livre = True
    except:
        pass


        
### Modo Livre -> Gráfico -> Simulação Livre
B_intensidade = 0
distancia_livre = 1
def atualiza_distancia_livre(s):
    global distancia_livre, B_intensidade, Tensao_hall, wt_slider, campo_magnetico_maximo, i, n_portadores, q, t
    distancia_livre = s.value
    B_intensidade = campo_magnetico_maximo / (distancia_livre**3)  # campo magnético em Tesla
    Tensao_hall = (B_intensidade * i) / (n_portadores * q * t)  # tensão Hall em Volts
    wt_slider.text = f"Dist. (cm): {distancia_livre:.2f}\n"

def iniciar_simulacao():
    global escopo_simulacao
    escopo_simulacao = True
    iniciar_livre.disabled = True
    resetar_livre.disabled = False

def resetar_simulacao():
    global key_simulacao, ha_objetos, campo_eletrico_ativo, campo_magnetico_ativo
    key_simulacao = False
    ha_objetos = False
    iniciar_livre.disabled = False
    resetar_livre.disabled = True
    opt_campo_eletrico.checked = True
    opt_campo_magnetico.checked = False
    for obj in scene.objects:
        obj.visible = False
    del bloco
    del placa_direita
    del placa_esquerda
    eletrons_moveis = []
    eletrons_acumulados = []
    scene.forward = vector(0, 0, -1)
    scene.up = vector(0, 1, 0)

    campo_magnetico_ativo = True
    campo_magnetico_ativo = False

def checkbox_campo_eletrico(evt):
    global campo_eletrico_ativo
    if evt.checked:
        campo_eletrico_ativo = True
    else:
        campo_eletrico_ativo = False

def checkbox_campo_magnetico(evt):
    global campo_magnetico_ativo
    if evt.checked:
        campo_magnetico_ativo = True
    else:
        campo_magnetico_ativo = False
    
####################################### Rodando ######################################

while True:
    rate(300)

##### Modo Livre -> Gráfico Livre
    if inicializacao_livre == True:
        esp_l1 = wtext(text="<br><br>")
        menu_campo_livre = menu(bind=define_campo_magnetico_maximo, align="left", choices=["Selecione Campo Mag.",
                           "0,002T (ímã de geladeira)", "1T (mini ímã de neodímio)", "14T (ímã secreto do LNNano)"])
        esp_l2 = wtext(text="<br><br>")
        instrucao_distancia_maxima = wtext(text="Distância máx. (cm, >1):", align="left")
        entrada = winput(bind=recebe_distancia_maxima, type="numeric", align="left")
        inicializacao_livre = False
        
    if key_grafico_livre == True and campo_magnetico_maximo != 0:
        esp_l2.delete()
        instrucao_distancia_maxima.delete()
        entrada.delete()
        menu_campo_livre.delete()

        al, bl, cl = dados_usuario(distancia_maxima, campo_magnetico_maximo, i, n_portadores, q, t)
        plotar_graficos(al, bl, cl, campo_magnetico_maximo)
        
        slider_grafico_livre = slider(bind=atualiza_distancia_livre, min=1, max=distancia_maxima, 
                               value=1, step=1, length=300, align="left")
        wt_slider = wtext(text=f"Dist. (cm): {slider_grafico_livre.value:.2f}\n")
        atualiza_distancia_livre(slider_grafico_livre)
        esp_l3 = wtext("", height=20)
        iniciar_livre = button(bind=iniciar_simulacao, text="Iniciar Simulação", disabled=False, align="left")
        resetar_livre = button(bind=resetar_simulacao, text="Resetar Simulação", disabled=True, align="left")
        esp_l4 = wtext(text="<br>")
        opt_campo_eletrico = checkbox(text="Campo Elétrico", bind=checkbox_campo_eletrico, checked=True, align="left")
        opt_campo_magnetico = checkbox(text="Campo Magnético", bind=checkbox_campo_magnetico, checked=False, align="left")
        
        modo_livre.disabled = False
        key_grafico_livre = False
        ha_grafico_livre = True

        
    
##### Simulação Geral - Escopo
    if escopo_simulacao == True:            
        
    # ========== Dados coletados ==========

    # Campo elétrico gerador da corrente
        A = w * t
        J = i / A
        E_intensidade = J / sigma
        E = vector(-E_intensidade, 0, 0)

    # ========== Visualização ==========
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

    # ========== Loop de simulação ==========
        tempo_inicial = clock()
        intervalo_geracao = 0.5  # segundos
        
        key_simulacao = True
        escopo_simulacao = False


    
###### Simulação Geral - Loop
    if key_simulacao == True:
        # Geração Periódica de Elétrons
        if clock() - tempo_inicial > intervalo_geracao:
            criar_eletron()
            tempo_inicial = clock()

    # Atualiza campo magnético
        B = vector(0, B_intensidade * 1e-4, 0)

    # Atualiza movimento
        for e in eletrons_moveis[:]:
            # Força elétrica (externa)
            F_elet = q * E if campo_eletrico_ativo else vector(0, 0, 0)

            # Força magnética
            F_mag = q * cross(e.vel, B) if campo_magnetico_ativo  else vector(0, 0, 0)
                
            # Campo Hall dinâmico
            delta_n = n_direita - n_esquerda
            # Campo Hall real (a partir do acúmulo de carga)
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

        ha_objetos = True
