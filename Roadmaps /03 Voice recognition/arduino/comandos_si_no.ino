#include <PDM.h>

#define BUFFER_SIZE 256
short sampleBuffer[BUFFER_SIZE];
volatile int samplesRead = 0;

void onPDMdata() {
  int bytesAvailable = PDM.available();
  if (bytesAvailable > BUFFER_SIZE * 2) {
    bytesAvailable = BUFFER_SIZE * 2;
  }
  PDM.read(sampleBuffer, bytesAvailable);
  samplesRead = bytesAvailable / 2;  // 16-bit samples
}

void setup() {
  Serial.begin(1000000);
  while (!Serial) {}

  // PDM mic
  PDM.onReceive(onPDMdata);
  PDM.begin(1, 16000);  // 16 kHz, mono

  // LEDs RGB de la Nano 33 BLE Sense
  pinMode(LEDR, OUTPUT);
  pinMode(LEDG, OUTPUT);
  pinMode(LEDB, OUTPUT);

  // Apagar todos (son activos en LOW)
  digitalWrite(LEDR, HIGH);
  digitalWrite(LEDG, HIGH);
  digitalWrite(LEDB, HIGH);
}

void loop() {
  // 1) Enviar audio a la PC
  if (samplesRead > 0) {
    Serial.write((uint8_t *)sampleBuffer, samplesRead * 2);
    samplesRead = 0;
  }

  // 2) Leer comandos de la PC para los LEDs
  while (Serial.available() > 0) {
    char c = Serial.read();

    if (c == 'S') {          // "si" → LED verde
      digitalWrite(LEDR, HIGH); // rojo OFF
      digitalWrite(LEDG, LOW);  // verde ON
    } else if (c == 'N') {   // "no" → LED rojo
      digitalWrite(LEDG, HIGH); // verde OFF
      digitalWrite(LEDR, LOW);  // rojo ON
    } else if (c == '0') {   // silencio / sin decisión → todo apagado
      digitalWrite(LEDR, HIGH);
      digitalWrite(LEDG, HIGH);
    }
  }
}

