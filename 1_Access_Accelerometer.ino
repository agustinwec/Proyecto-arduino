/*
  Este ejemplo lee los valores de aceleración 
  en dirección relativa y grados desde el sensor LSM9DS1 
  y los imprime en el monitor
*/

#include <Arduino_LSM9DS1.h>

float x, y, z;
int degreesX = 0;
int degreesY = 0;

void setup() {
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Started");

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  Serial.print("Frecuencia de muestreo del acelerómetro = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println("Hz");
}

void loop() {

  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);

  }

  if (x > 0.1) {
    x = 100 * x;
    degreesX = map(x, 0, 97, 0, 90);
    Serial.print("inclinando hacia arriba ");
    Serial.print(degreesX);
    Serial.println("°");
  }
  if (x < -0.1) {
    x = 100 * x;
    degreesX = map(x, 0, -100, 0, 90);
    Serial.print("Inclinando hacia abajo ");
    Serial.print(degreesX);
  Serial.println("°");
  }
  if (y > 0.1) {
    y = 100 * y;
    degreesY = map(y, 0, 97, 0, 90);
    Serial.print("Inclinando hacia la izquierda ");
    Serial.print(degreesY);
    Serial.println("°");
  }
  if (y < -0.1) {
    y = 100 * y;
    degreesY = map(y, 0, -100, 0, 90);
    Serial.print("Inclinando hacia la derecha ");
    Serial.print(degreesY);
    Serial.println("°");
  }
  delay(1000);
}
