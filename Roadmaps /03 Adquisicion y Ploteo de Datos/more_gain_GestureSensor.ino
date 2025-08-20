/*
  Este ejemplo lee los datos de gestos del sensor APDS-9960 integrado del Nano 33 BLE Sense
  e imprime los gestos detectados en el monitor serie.
  Además, se modifica la ganancia del sensor de color/ALS.
*/

#include <Arduino_APDS9960.h>
#include <Wire.h>

#define APDS9960_I2C_ADDR 0x39
#define APDS9960_CONTROL  0x8F

// Función para configurar la ganancia ALS (color/luz)
// gain = 0 → 1x, 1 → 4x, 2 → 16x, 3 → 64x
void setALSGain(uint8_t gain) {
  Wire.beginTransmission(APDS9960_I2C_ADDR);
  Wire.write(APDS9960_CONTROL);
  Wire.write(gain & 0x03);  // Solo los 2 bits bajos controlan la ganancia
  Wire.endTransmission();
}

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

  // Configurar la ganancia ALS en 16x
  Wire.begin();
  setALSGain(3);   // 0=1x, 1=4x, 2=16x, 3=64x
  Serial.println("Ganancia ALS configurada a 64x");

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

