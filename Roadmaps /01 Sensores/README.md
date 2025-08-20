# Lectura de temperatura y humedad 🌡️



## Objetivos
Los objetivos de este proyecto son:

-   Utilizar el sensor HTS221.
-   Utilizar la biblioteca HTS221.
-   Imprimir los valores de temperatura y humedad en el Monitor Serial del Arduino IDE
-   Crea tu propio monitor de temperatura y humedad

## imagen de descargar el 

## Configuraciones previas

**1. Instalacion**

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



# Reconocimiento de gestos

## Objetivos
Los objetivos de este proyecto son:

-   Descubra qué es un sensor APDS9960.
-   Utilice la biblioteca APDS9960.
-   Aprenda cómo generar datos sin procesar del sensor Arduino Nano 33 BLE Sense.
-   Crea tu propio monitor de detección de gestos.
-   Aprenda a controlar el LED incorporado y el LED RGB mediante gestos con las manos.

## Sensor APDS9960
El chip **APDS9960** permite medir la proximidad digital y la luz ambiental, así como detectar colores y gestos RGB.

![enter image description here](https://docs.arduino.cc/static/9b60e96cca5c9fe7bba5ddfed3abf760/29114/nano33BS_07_sensor.png)

## Creando el programa

### Biblioteca APDS9960

Para acceder a los datos del módulo APDS9960, necesitamos instalar la biblioteca APDS9960. Hagamos clic en la pestaña **Library** y busquemos la biblioteca **APDS9960** y la instalamos.


**Programar**
incluimos la librería APDS9960 que habíamos instalado
Y dentro de setup inicializamos 

   ```cpp
    #include <Arduino_APDS9960.h>
    void  setup() {
    }
    void  loop() {
    }
   ```

**Setup**
En el setup inicializamos: 

 -  Los pines de los LEDs (rojo, verde, azul y el LED integrado).
-   La comunicación serial  `Serial.begin(9600)`.
-   El sensor APDS-9960 con `APDS.begin()`

```cpp
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(LEDR, OUTPUT);
  pinMode(LEDG, OUTPUT);
  pinMode(LEDB, OUTPUT);
  //se encienden los LEDs RGB para indicar que están listos.
  digitalWrite(LEDR, HIGH);
  digitalWrite(LEDG, HIGH);
  digitalWrite(LEDB, HIGH);

  Serial.begin(9600);
  while (!Serial);

  if (!APDS.begin()) {
    Serial.println("Error initializing APDS-9960 sensor!");
  }

  Serial.println("Detectando gestos ...");
}
```
**Loop**
En el loop :
 

 - Se verifica si hay un gesto disponible con  **APDS.gestureAvailable()**
 - Se lee el gesto con **APDS.readGesture()**
 - Según el gesto detectado, se enciende un **LED** específico por un segundo y se imprime el tipo de gesto en el monitor serial

  ```cpp
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
   ```
	
### Posición de la placa

Para que los gestos se detecten correctamente, la placa debe estar orientada así:

-   **ARRIBA**: del conector USB hacia la antena
-   **ABAJO**: de la antena hacia el conector USB
-   **IZQUIERDA**: del lado de los pines analógicos al lado de los pines digitales
-   **DERECHA**: del lado de los pines digitales al lado de los pines analógicos

### Ejecutar el código ▶️

1.  Subí el código a la placa.
2.  Abrí el **Serial Monitor** en el IDE de Arduino.
3.  Realizá gestos frente al sensor y observá los resultados impresos y los LEDs encendidos.

#### Qué aprendimos:

-   Cómo usar el sensor APDS-9960 para detectar gestos.
-   Cómo controlar LEDs de la placa Arduino
-   Uso de la biblioteca APDS-9960.



# Captura y Reproducción de Audio con Arduino Nano 33 BLE Sense + Python

## Objetivo

Grabar una muestra de audio desde el micrófono digital del Arduino Nano 33 BLE Sense, transmitirlo por puerto serial a una computadora, guardarlo como archivo  y reproducirlo usando Python. 

## PDM
El Arduino usa la librería  para capturar audio a 16 kHz en formato mono. Las muestras de audio (16 bits) se envían por el puerto serial como bytes.

## Python 
Python recibe los datos, reconstruye las muestras, las guarda como archivo  y las reproduce.

### Librerias que vamos a utilizar:
-   pyserial
-   numpy
-   wave
-   sounddevice
- PDM (En Arduino IDE)

## Código Arduino:

-   `PDM.begin(1, 16000)` configura el micrófono en mono a 16 kHz.
-   Las muestras se transmiten como pares de bytes

  ```  cpp
  #include <PDM.h>

#define BUFFER_SIZE 512
short sampleBuffer[BUFFER_SIZE];
volatile int samplesRead;

void setup() {
  Serial.begin(115200);
  while (!Serial);

  PDM.onReceive(onPDMdata);
  PDM.begin(1, 16000);  // 16kHz, mono
}

void loop() {
  if (samplesRead > 0) {
    Serial.write((byte*)sampleBuffer, samplesRead * 2);  // 16-bit samples
    samplesRead = 0;
  }
}

void onPDMdata() {
  int bytesAvailable = PDM.available();
  PDM.read(sampleBuffer, bytesAvailable);
  samplesRead = bytesAvailable / 2;
}
   ```

## Código Python:

Recibe los datos, los convierte en audio y los guarda:





```cpp
import serial, wave, numpy as np, sounddevice as sd

COM_PORT = 'COM3'   # Cambiar según el sistema
BAUD_RATE = 115200
SAMPLE_RATE = 16000
DURATION_SECONDS = 10
FILENAME = 'grabacion.wav'

ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
ser.reset_input_buffer()

num_samples = SAMPLE_RATE * DURATION_SECONDS
audio = []

print("Grabando audio...")

while len(audio) < num_samples:
    if ser.in_waiting >= 2:
        low_byte = ser.read(1)
        high_byte = ser.read(1)
        sample = int.from_bytes(low_byte + high_byte, byteorder='little', signed=True)
        audio.append(sample)

ser.close()
print("✅ Grabación terminada.")

audio_np = np.array(audio, dtype=np.int16)

with wave.open(FILENAME, 'wb') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(audio_np.tobytes())

print(f"📂 Archivo guardado como: {FILENAME}")

sd.play(audio_np, SAMPLE_RATE)
sd.wait()
print("🔊 Reproducción terminada.")
```
-   Cada muestra se reconstruye a partir de dos bytes.
-   El archivo  .wav  se guarda con 1 canal, 16 bits por muestra y 16 kHz.
-   La reproducción es opcional y se puede desactivar si no se desea.
