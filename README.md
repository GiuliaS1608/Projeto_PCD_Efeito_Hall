# HELLO — Hall Effect Learning & Observation
 
 **HELLO** é um projeto interdisciplinar que combina física, ciência de dados e programação para simular e analisar o **Efeito Hall** de forma interativa, visual e acessível. Desenvolvido com Python, VPython e Arduino, o projeto permite explorar o comportamento de cargas elétricas em um campo magnético e compreender a variação da tensão Hall com a distância de um ímã.
 
##Objetivo
 
Tornar o Efeito Hall mais compreensível e visual através de:
- Simulação do movimento dos elétrons sob campos elétrico e magnético
- Análise gráfica da relação entre **tensão Hall** e **distância do ímã**
- Coleta de dados experimentais com **sensor Hall + Arduino**
- Comparação entre dados teóricos e experimentais
 
##Tecnologias Utilizadas
 
- **Python 3**
- **VPython** – visualização 3D de simulações físicas
- **gcurve (vpython.graph)** – gráficos interativos
- **Sensor Hall + Arduino** – coleta de dados experimentais
- **pySerial** – comunicação com Arduino via porta serial
 
## Como Funciona
 
### Modo Teórico 
- Usuário define a distância entre o ímã e o condutor
- O programa calcula o campo magnético (∝ 1/d³) e a tensão Hall
- Os dados são plotados automaticamente
 
### Modo Experimental 
- Sensor Hall coleta a tensão Hall em distâncias específicas (1–5 cm)
- O Arduino envia os dados via porta serial
- O programa interpreta e plota os resultados medidos
  
