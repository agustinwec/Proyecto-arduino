/*
 Arduino LSM9DS1 - Magnetómetro

Este ejemplo lee los valores del magnetómetro del sensor LSM9DS1 
y muestra en el LED integrado según la intensidad del campo magnético que rodea los dispositivos eléctricos.

*/


#include <Arduino_LSM9DS1.h>
float x,y,z, ledvalue;

void setup() {
  IMU.begin();
}

void loop() {
  
  // read magnetic field in all three directions
  IMU.readMagneticField(x, y, z);
  
  if(x < 0)
  {
    ledvalue = -(x);
  }
  else{
    ledvalue = x;
  }
  
  analogWrite(LED_BUILTIN, ledvalue);
  delay(500);
}
