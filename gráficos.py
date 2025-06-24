from vpython import graph, gcurve, color
import serial
import time

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


#  PARTE ARDUÍNO


def plotar_graficos(distancias, campos_por_distancia, dados_tensao):
    """
    Plota gráfico:
     Tensão Hall x Distância
    """

    graf = graph(title="Tensão Hall x Distância", xtitle="Distância (cm)", ytitle="Tensão Hall (V)", width=600, height=400)
    curva2 = gcurve(color=color.blue, label="Dados")
    for d in distancias:
        tensao = dados_tensao[d][0] if dados_tensao[d] else 0
        curva2.plot(d, tensao)

if __name__ == "__main__":
    print("Experimento do Efeito Hall - escolha o modo de entrada de dados")
    modo = input("Digite '1' para inserir dados manualmente ou '2' para coletar do Arduino: ")

    if modo == '1':
        distancias, campos_por_distancia, dados_tensao = receber_dados_usuario()
    #elif modo == '2':
        #distancias, campos_por_distancia, dados_tensao = receber_dados_arduino()
        if distancias is None:
            print("Falha na leitura do Arduino. Encerrando.")
            exit()
    else:
        print("Opção inválida. Encerrando.")
        exit()

    print("Gerando gráficos...")
    plotar_graficos(distancias, campos_por_distancia, dados_tensao)
    input("Pressione Enter para sair e fechar os gráficos...")


