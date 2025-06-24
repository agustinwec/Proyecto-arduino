float old_temp = 0;
float old_hum = 0;
bool first_time = true; 


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
  // Se leen los valores del sensor
  float temperature_Celcius = HTS.readTemperature();
  float humidity    = HTS.readHumidity();

  // Agregamos para que la temperatura también aparezca en grados Fahrenheit
  float temperature_Fahrenheit = temperature_Celcius * 1.8 + 32;

  // Verificar si el rango de valores de temperatura es superior a 0,5 ºC
  // y si el rango de valores de humedad es superior al 1 %
  if (first_time || abs(old_temp - temperature_Celcius) >= 0.5 || abs(old_hum - humidity) >= 1)
  { 
    old_temp = temperature_Celcius;
    old_hum = humidity;
    first_time = false; 

  // Imprimimos los valores
    Serial.print("Temperatura en celcius = ");
    Serial.print(temperature_Celcius);
    Serial.println(" °C");

    Serial.print("Temperatura en Fahrenheit = ");
    Serial.print(temperature_Fahrenheit);
    Serial.println(" °F");
  
    Serial.print("Humidity    = ");
    Serial.print(humidity);
    Serial.println(" %");
  
    Serial.println();
  }
  delay(1000);
}
