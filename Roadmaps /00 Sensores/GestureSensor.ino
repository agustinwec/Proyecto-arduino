/*
  Este ejemplo lee los datos de gestos del sensor APDS-9960 integrado del Nano 33 BLE Sense e imprime los gestos detectados en el monitor serie.

La posicion de la placa debe ser la siguiente:
- ARRIBA: del conector USB hacia la antena
- ABAJO: de la antena hacia el conector USB
- IZQUIERDA: del lado de los pines analógicos al lado de los pines digitales
- DERECHA: del lado de los pines digitales al lado de los pines analógicos

*/

#include <Arduino_APDS9960.h>

void setup() {

  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(LEDR, OUTPUT);
  pinMode(LEDG, OUTPUT);
  pinMode(LEDB, OUTPUT);

  digitalWrite(LEDR, HIGH);
  digitalWrite(LEDG, HIGH);
  digitalWrite(LEDB, HIGH);

  
  Serial.begin(9600);
  while (!Serial);

  if (!APDS.begin()) {
    Serial.println("Error initializing APDS-9960 sensor!");
  }

  Serial.println("Detecting gestures ...");
}
void loop() {
  if (APDS.gestureAvailable()) {

    int gesture = APDS.readGesture();

    switch (gesture) {
      case GESTURE_UP:
        digitalWrite(LEDR, LOW);
        delay(1000);
        digitalWrite(LEDR, HIGH);
        Serial.println("Gesto hacia arriba detectado");
        break;

      case GESTURE_DOWN:
        digitalWrite(LEDG, LOW);
        delay(1000);
        digitalWrite(LEDG, HIGH);
        Serial.println("Gesto hacia abajo detectado");
        break;

      case GESTURE_LEFT:
        digitalWrite(LEDB, LOW);
        delay(1000);
        digitalWrite(LEDB, HIGH);
        Serial.println("Gesto hacia la izquierda detectado");
        break;

      case GESTURE_RIGHT:
        digitalWrite(LED_BUILTIN, HIGH);
        delay(1000);
        digitalWrite(LED_BUILTIN, LOW);
        Serial.println("Gesto hacia la derecha detectado");
        break;

      default:
        
        break;
    }
  }
}
