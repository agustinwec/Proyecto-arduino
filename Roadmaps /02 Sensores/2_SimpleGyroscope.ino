/*
 Arduino LSM9DS1 - Aplicación de giroscopio

Este ejemplo lee los valores del giroscopio del sensor LSM9DS1 
y los imprime en el monitor.

*/

#include <Arduino_LSM9DS1.h>

float x, y, z;
int plusThreshold = 30, minusThreshold = -30;

void setup() {
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Started");

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
  Serial.print("Gyroscope sample rate = ");
  Serial.print(IMU.gyroscopeSampleRate());
  Serial.println(" Hz");
  Serial.println();
  Serial.println("Gyroscope in degrees/second");
}
void loop() {
  
  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(x, y, z);
  }
  if(y > plusThreshold)
  {
    Serial.println("Inclinacion hacia el frente");
    delay(500);
  }
  if(y < minusThreshold)
  {
    Serial.println("Inclinacion hacia atras");
    delay(500);
  }
  if(x < minusThreshold)
  {
    Serial.println("Inclinacion derecha");
    delay(500);
  }
    if(x > plusThreshold)
  {
    Serial.println("inclinacion izquierda");
    delay(500);
  }
  
}
