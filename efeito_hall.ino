// Pino do sensor como o A0
const int pinoSensor = A0;

// Valor recebido pelo conversor A/D
int valorHall1  = 0;
int valorHall2  = 0;
int valorHall3  = 0;
int valorHall4  = 0;
int valorHall5  = 0;

// Valor_medido convertido para tensao
float tensao1 = 0;
float tensao2 = 0;
float tensao3 = 0;
float tensao4 = 0;
float tensao5 = 0;

void setup() {
  //inicia comunicação serial
  Serial.begin(9600);
  pinMode(pinoSensor, INPUT);
}

void loop() { 
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');  // Lê o comando até encontrar quebra de linha
    
    if (comando == "PrimeiraMedida") {
      int valorHall1 = analogRead(pinoSensor);    // Lê o valor analógico (0-1023)
      float tensao1 = valorHall1 * (5.0 / 1023.0);   // Converte para tensão (0-5V)

      Serial.println(tensao1, 4); 
    }

    if (comando == "SegundaMedida") {
      int valorHall2 = analogRead(pinoSensor);    // Lê o valor analógico (0-1023)
      float tensao2 = valorHall2 * (5.0 / 1023.0);   // Converte para tensão (0-5V)

      Serial.println(tensao2, 4); 
    }

    if (comando == "TerceiraMedida") {
      int valorHall3 = analogRead(pinoSensor);    // Lê o valor analógico (0-1023)
      float tensao3 = valorHall3 * (5.0 / 1023.0);   // Converte para tensão (0-5V)

      Serial.println(tensao3, 4); 
    }

    if (comando == "QuartaMedida") {
      int valorHall4 = analogRead(pinoSensor);    // Lê o valor analógico (0-1023)
      float tensao4 = valorHall4 * (5.0 / 1023.0);   // Converte para tensão (0-5V)

      Serial.println(tensao4, 4); 
    }

    if (comando == "QuintaMedida") {
      int valorHall5 = analogRead(pinoSensor);    // Lê o valor analógico (0-1023)
      float tensao5 = valorHall5 * (5.0 / 1023.0);   // Converte para tensão (0-5V)

       Serial.println(tensao5, 4); 
    }
  }
}
