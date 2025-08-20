# Lectura de temperatura y humedad 🌡️



## Objetivos
Los objetivos de este proyecto son:

-   Utilizar el sensor HTS221.
-   Utilizar la biblioteca HTS221.
-   Imprimir los valores de temperatura y humedad en el Monitor Serial del Arduino IDE
-   Crea tu propio monitor de temperatura y humedad

## imagen de descargar el 

## Creando el programa

**1. Configuración**

Para empezar, abrimos el [Arduino IDE](https://www.arduino.cc/en/software/).

Con el editor abierto, observemos la columna izquierda. Aquí vemos un par de iconos. Hagamos clic en el icono **de la placa Arduino**. Y escribimos "Mbed OS Nano" y donde aparece Arduino Mbed OS Nano Boards, apretamos instalar. 
![enter image description here](https://github.com/agustinwec/Proyecto-arduino/blob/main/Roadmaps%20/01%20Sensores/Images/Captura%20de%20pantalla0.png?raw=true)

**2. Conexión de la placa**

Ahora, conecta el Arduino Nano 33 BLE Sense al ordenador para comprobar que el Editor lo reconoce. Nos dirigimos a la seccion Tools o herramientas, vamos a donde dice Board. Elegimos la opción Arduino Mbed OS Nano Boards y seleccionamos la placa Arduino Nano 33 Ble
![enter image description here](https://github.com/agustinwec/Proyecto-arduino/blob/main/Roadmaps%20/01%20Sensores/Images/Captura%20de%20pantalla2.png?raw=true)


Después vamos a opción "Port" para seleccionar el puerto en el que esta conectado la placa de Arduino.
![enter image description here](https://github.com/agustinwec/Proyecto-arduino/blob/main/Roadmaps%20/01%20Sensores/Images/Captura%20de%20pantalla4.png?raw=true)

**3. Instalamos las librerias que necesitamos**

Hacemos clic en la pestaña **Library** , buscamos la biblioteca **HTS221** y apretamos instalar 

![enter image description here](https://github.com/agustinwec/Proyecto-arduino/blob/main/Roadmaps%20/01%20Sensores/Images/Captura%20de%20pantalla1.png?raw=true)

**4. Programar**
Antes del void setup, incluimos la libreria HTS221 que habíamos instalado

   ```cpp
    #include  <Arduino_HTS221.h>
    void  setup() {
    }
    void  loop() {
    }
   ```

En la parte de **void setup** vamos a colocar codigo que solo se va a ejecutar 1 vez, que va ser cuando recien se conecta o prenda la placa

En cambio en el **loop** vamos a poner el código que se va ir repitiendo al ejecutarse, ya que es un ciclo. 


**Setup**
La función **Serial.begin**  Inicia la comunicación **serial** entre la placa y la PC

La función **HTS.begin** inicializa el sensor HTS

Así que agregamos el siguiente codigo en el **Setup**:
```cpp
void setup() {
  Serial.begin(9600);
  while (!Serial);  //Esto espera hasta que el puerto serial esté listo

  if (!HTS.begin()) {  //si el sensor no se inicializó correctamente va enviar un mensaje del fallo
    Serial.println("Failed to initialize humidity temperature sensor!");
    while (1); 
  }
}
```


inicializamos  las siguientes variables antes de setup()

   ```cpp
    float old_temp = 0;
    float old_hum = 0;
    bool first_time = true; // nos va a servir para mostrar ni bien empiece el programa  

```
**loop**
La función **HTS.readTemperature()** lee los valores de temperatura
y  **HTS.readHumidity()** lee  el porcentaje de humedad


En el loop declaramos las variables de la temperatura y humedad

   ```cpp
      
    void loop() {
	  // read lee los valores del sensor
	  float temperature = HTS.readTemperature();
	  float humidity    = HTS.readHumidity();
		
		// Agregamos para que la temperatura también aparezca en grados Fahrenheit
	  float temperature_Fahrenheit = temperature_Celcius * 1.8 + 32;
	  
	  // comprobamos si los valores del rango de temperatura y humedad cambiaron
	  // solo se va mostrar la temperatura y humedad si hubo algun cambio o si es la primera vez que se inicia
      if(first_time || abs(old_temp - temperature_Celcius) >= 0.5 || abs(old_hum - humidity) >= 1)
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
	  
	    Serial.print("Humedad    = ");
	    Serial.print(humidity);
	    Serial.println(" %");
	  
	    Serial.println();
	  }
	  delay(1000); 
	}
   ```
	


## Ejecutar el codigo
Compilamos y ejecutamos el código. Nos dirigimos a la parte superior derecha y apretamos el icono del **Serial Monitor**
![enter image description here](https://github.com/agustinwec/Proyecto-arduino/blob/main/Roadmaps%20/01%20Sensores/Images/Captura%20de%20pantalla5.png?raw=true)


## Que hicimos:

 - Aprendimos que **Setup** se usa para inicializar y el **Loop** para todo lo que se ira repitiendo
 
 - Aprendimos cómo leer valores de temperatura y humedad del sensor **HTS221** usando la [biblioteca HTS221](https://github.com/arduino-libraries/Arduino_HTS221)
 - Aprendimos cómo usar el sensor integrado en la placa Arduino Nano 33 BLE Sense, para medir e imprimir valores de humedad y temperatura del ambiente.
