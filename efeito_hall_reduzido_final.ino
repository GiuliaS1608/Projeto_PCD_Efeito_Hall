// Pino do sensor como o A0
const int pinoSensor = A0;

// Valor recebido pelo conversor A/D
int valorHall  = 0;

// Valor_medido convertido para tensao
float tensao = 0;


void setup() {
  //inicia comunicação serial
  Serial.begin(9600);
  pinMode(pinoSensor, INPUT);
}

void loop() { 
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');  // Lê o comando até encontrar quebra de linha
    
    if (comando == "Medir") {
      int valorHall= analogRead(pinoSensor);    // Lê o valor analógico (0-1023)
      float tensao = valorHall * (5.0 / 1023.0);   // Converte para tensão (0-5V)

      Serial.println(tensao, 4); 
    }
  }
}
