# H.E.L.L.O., world! — Hall Effect Lab for Learning and Observation
---
**Integrantes:** Edélio Gabriel Magalhães de Jesus, Gisela Ceresér Kassick, Giulia Sales Ferreira, Leonardo Ritchielly dos S Vieira

**Instituição:** Ilum- Escola de Ciência- CNPEM

**Disciplina:** Prática em Ciência de Dados

**Professores orientadores:** Daniel Roberto Cassar, James Moraes de Almeida e Leandro Nascimento Lemos

---

 **H.E.L.L.O., world!** é um projeto interdisciplinar que combina física, ciência de dados e programação para simular e analisar o **Efeito Hall** de forma interativa, visual e acessível. Desenvolvido com Python, VPython e Arduino, o projeto permite explorar o comportamento de cargas elétricas em um campo magnético e compreender a variação da tensão Hall com a distância de um ímã. 

---

## Sumário

- [Sobre o projeto](#sobre-o-projeto)
- [Como Executar](#como-executar)
- [Especificações Técnicas](#especificações-técnicas)
- [Referências](#referências)
- [Professores orientadores](#professores-orientadores)
- [Contribuições da Equipe](#contribuições-da-equipe)

---

## Sobre o projeto

O **Efeito Hall** é um fenômeno no qual uma diferença de potencial é gerada perpendicularmente a um condutor percorrido por corrente elétrica, quando submetido a um campo magnético. A partir dos códigos criados no presente projeto, o **HELLO, world!** tem como **objetivo** tornar o Efeito Hall mais **compreensível** e visual através de: 
- Simulação 3D do movimento dos elétrons sob campos elétrico e magnético, com o VPython
- Análise **gráfica** da relação entre **tensão Hall** e **distância do ímã** 
- Possibilidade de coleta de dados experimentais com **sensor Hall + Arduino** 
- Analisar e comparar graficamente tensões Hall experimentais e teóricas, a partir de seus dois modos de funcionamento:
  - **Teórico**: baseia-se na relação B ∝ 1/d³
  - **Experimental**: coleta dados em tempo real do sensor 
- Fornecer uma interface educacional para explorar o fenômeno de forma dinâmica.
---

## Como Executar

### Requisitos

- Python 3
- Arduino IDE  
- Bibliotecas: `vpython`, `serial`, `time`  
- Protoboard e 3 jumpers macho-macho  
- Sensor Hall SS49E  
- Ímã (para testes experimentais)  


###  Instalação

```bash
git clone https://github.com/EdelioGabriel/Projeto_PCD_Efeito_Hall.git
cd Projeto_PCD_Efeito_Hall
pip install vpython
pip install serial
pip install time
```

### Executando o Código

O repositório tem três arquivos de códigos principais: efeito_hall_reduzido_final.ino, codigo_reduzido_final.py e interface_teorico.py

**1. Carregando o código do Arduino** - efeito_hall_reduzido_final.ino

- Com o sensor Hall voltado para você (inscrição **"49E/455BG"** visível), monte o seguinte circuito:
  - **Perna esquerda** → Conecte à porta **5V** do Arduino (via jumper)
  - **Perna central** → Conecte ao **GND** (terra)
  - **Perna direita** → Conecte à entrada **A0** (analógica)
- Conecte o Arduino ao computador pela **porta COM3** e carregue o código `efeito_hall_reduzido_final.ino` usando a Arduino IDE.

**2. Modo Experimental ou Teórico (VSCode)**  - codigo_reduzido_final.py

  - Execute o arquivo `codigo_reduzido_final.py` no VSCode.  
  - O programa irá coletar dados do sensor (modo experimental) ou gerar dados simulados (modo teórico), e exibir o gráfico resultante e a simulação desejada.

**3. Modo Teórico com Interface Interativa (GlowScript)**  - interface_teorico.py

  - Execute o arquivo `interface_teorico.py` no ambiente [GlowScript](https://www.glowscript.org/).  
  - O usuário poderá selecionar diferentes ímãs, ajustar distâncias e visualizar a dinâmica das cargas elétricas sob o campo magnético.

---

## Especificações Técnicas

### Linguagens e Tecnologias

- **Python** – Análise de dados, simulações físicas
- **VPython / GlowScript** – Visualização 3D interativa
- **C++ (Arduino IDE)** – Leitura do sensor e comunicação serial

###  Bibliotecas Utilizadas
- Python 3
- VPython: Visualização física 3D         
- gcurve: Gráficos dinâmicos no VPython 
- Serial: Comunicação com a porta COM  
- Time: Controle de tempo e delays 

###  Modelo Físico

####  Cálculo da Tensão Hall com dados manuais:

V<sub>H</sub> = (I × B) / (n × q × t)

Onde:

- \( I \): corrente elétrica  
- \( B \): campo magnético  
- \( n \): densidade de portadores de carga  
- \( q \): carga do elétron  
- \( t \): espessura do condutor
- Sensitividade (S) do sensor = n x q x t

####  Cálculo da Tensão Hall com dados do Arduino:
V<sub>H</sub>  = [V<sub>lido</sub> (5.0 / 1023.0)] - 2.5

Onde:
- 2.5 equivale ao valor Offset do sistema do Arduino
- V<sub>lido</sub> = valor bruto recebido na porta analógica do Arduino


#### Força de Lorentz:
F = q(E + v × B)

Onde: 
- F: Força (vetor)
- q: Carga elétrica
- E: Campo elétrico (vetor)
- v: Velocidade (vetor)
- B: Campo magnético (vetor)
- ×: Produto vetorial
  
---
## Referências
- HONEYWELL Sensing and Control. SS49E Linear Hall Effect Sensor. Version 2.00, May 2001. Disponível em: https://sensing.honeywell.com/hall-effect-sensors-ss49e. Acesso em: 06 jun. 2025.

- RYNDACK COMPONENTES. Usando um sensor de efeito Hall. Blog Ryndack, 20 mar. 2025. Disponível em: https://blog.ryndackcomponentes.com.br/usando-um-sensor-de-efeito-hall/. Acesso em: 06 jun. 2025.

- UNIVERSIDADE DE SÃO PAULO. Aula 2.2: propriedades elétricas – efeito Hall. São Paulo: EEL-USP, 2012. Disponível em: https://sistemas.eel.usp.br/docentes/arquivos/5840726/LOM3035/Aula2.2-PropriedadesEletricas-EfeitoHall.pdf. Acesso em: 6 jun. 2025.

- UNIVERSIDADE FEDERAL DO RIO GRANDE DO SUL. O efeito Hall. Instituto de Física – FIS142, módulo 8. 2004. Disponível em: https://www.if.ufrgs.br/tex/fis142/mod08/m_s03.html. Acesso em: 24 jun. 2025.

- SANTOS, Ronilson Sousa.
Análise experimental do efeito Hall em semicondutores. 2023. Trabalho de Conclusão de Curso (Graduação em Física) - Universidade Federal do Tocantins, Porto Nacional, 2023.
Disponível em: https://umbu.uft.edu.br/bitstream/11612/6356/1/RONILSON%20SOUSA%20SANTOS-TCC-F%c3%8dSICA.pdf.
Acesso em: 11 jun. 2025.



---
## Professores orientadores

<table>
  <tr>
    <td align="center">
      <a href="#" title="Prof. Daniel R. Cassar">
        <img src="https://avatars.githubusercontent.com/u/9871905?v=4" width="100px;" alt="Foto do Daniel do Github"/><br>
          <a href="https://github.com/drcassar"><b>Prof. Dr. Daniel R. Cassar<b></a>
      </a>
    </td>
    <td align="center">
      <a href="#" title="Prof. James M. de Almeida">
        <img src="https://avatars.githubusercontent.com/u/108157661?v=4" width="100px;" alt="Foto do James do Github"/><br>
          <a href="https://github.com/jamesmalmeida"><b>Prof. Dr. James M. de Almeida<b></a>
      </a>
    </td>
    <td align="center">
      <a href="#" title="Prof. Leandro N. Lemos">
        <img src="https://avatars.githubusercontent.com/u/1894434?v=4" width="100px;" alt="Foto do Leandro do Github"/><br>
          <a href="https://github.com/Velky2"><b>Prof. Dr. Leandro N. Lemos<b></a>
      </a>
    </td>
  </tr>
</table>

---
## Contribuições da equipe
<table>
  <tr>
    <td align="center">
      <a href="#" title="Edélio G. M. de Jesus">
        <img src="https://avatars.githubusercontent.com/u/164672308?v=4" width="100px;" alt="Foto do Edélio no Github"/><br>
        <a href="https://github.com/EdelioGabriel"><b>Edélio G. M. de Jesus</b></a>
      </a>
    </td>
    <td align="center">
      <a href="#" title="Gisela C. Kassick">
        <img src="https://avatars.githubusercontent.com/u/164672308?v=4" width="100px;" alt="Foto da Gisela no Github"/><br>
        <a href="https://github.com/GiselaCK"><b>Gisela C. Kassick</b></a>
      </a>
    </td>
        <td align="center">
      <a href="#" title="Giulia S. Ferreira">
        <img src="https://avatars.githubusercontent.com/u/164672308?v=4" width="100px;" alt="Foto da Giulia no Github"/><br>
        <a href="https://github.com/GiuliaS1608"><b>Giulia S. Ferreira</b></a>
      </a>
    </td>
    <td align="center">
      <a href="#" title="Leonardo R.">
        <img src="https://avatars.githubusercontent.com/u/164672308?v=4" width="100px;" alt="Foto da Giulia no Github"/><br>
        <a href="https://github.com/LeoRitch"><b>Leonardo R. dos S. Vieira</b></a>
      </a>
    </td>
  </tr>
</table>


- Edélio Gabriel Magalhães de Jesus: criação da simulação 3d do efeito Hall
- Gisela Ceresér Kassick: programação do Arduino e do código de medição e recebimentos de dados experimentais
- Giulia Sales Ferreira: criação do código de recebimento de dados teóricos e plotagem de gráficos
- Leonardo Ritchielly dos S Vieira: criação da interface do código do Glowscript

Os documentos do trabalho (Readme, pdfs explicativos e apresentação) foram feito em conjunto pelo grupo.

  
