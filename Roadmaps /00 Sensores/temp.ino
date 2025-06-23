float old_temp = 0;
float old_hum = 0;


#include <Arduino_HTS221.h>

void setup() {
  Serial.begin(9600);
  while (!Serial);

  if (!HTS.begin()) {
    Serial.println("Failed to initialize humidity temperature sensor!");
    while (1);
  }
}

void loop() {
  // read all the sensor values
  float temperature_Celcius = HTS.readTemperature();
  float humidity    = HTS.readHumidity();

  // Verificar si el rango de valores de temperatura es superior a 0,5 ºC
  // y si el rango de valores de humedad es superior al 1 %
  if (abs(old_temp - temperature_Celcius) >= 0.5 || abs(old_hum - humidity) >= 1)
  { 
    old_temp = temperature_Celcius;
    old_hum = humidity;

  // print each of the sensor values
    Serial.print("Temperature = ");
    Serial.print(temperature_Celcius);
    Serial.println(" °C");
  
    Serial.print("Humidity    = ");
    Serial.print(humidity);
    Serial.println(" %");
  
    // print an empty line
    Serial.println();
  }
  
  Serial.print("Temperature = ");
  Serial.print(temperature_Celcius);
  Serial.println(" °C");

  Serial.print("Humidity    = ");
  Serial.print(humidity);
  Serial.println(" %");

  // print an empty line
  Serial.println();

  // wait 1 second to print again
  delay(1000);
}
