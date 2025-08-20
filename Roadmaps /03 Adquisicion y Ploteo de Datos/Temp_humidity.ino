#include <Arduino_HTS221.h>

float old_temp = 0;
float old_hum = 0;
bool first_time = true;

void setup() {
  Serial.begin(9600);
  while (!Serial);

  if (!HTS.begin()) {
    Serial.println("Failed to initialize humidity temperature sensor!");
    while (1);
  }
}

void loop() {
  float temperature_Celcius = HTS.readTemperature();
  float humidity = HTS.readHumidity();

  // Emitir solo cuando hay cambios significativos
  if (first_time || abs(old_temp - temperature_Celcius) >= 0.5 || abs(old_hum - humidity) >= 1) {
    old_temp = temperature_Celcius;
    old_hum = humidity;
    first_time = false;

    // Imprimir en formato CSV: tiempo, temperatura, humedad
    Serial.print(millis());
    Serial.print(",");
    Serial.print(temperature_Celcius, 2);
    Serial.print(",");
    Serial.println(humidity, 2);
  }

  delay(1000); // cada segundo
}
