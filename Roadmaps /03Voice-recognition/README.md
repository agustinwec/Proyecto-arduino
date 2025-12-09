# Reconocimiento de voz. Palabras si y no

Este proyecto hace reconocimiento de palabras clave **"sí"** y **"no"** usando el micrófono PDM del **Arduino Nano 33 BLE Sense**.
El Arduino **solo pasa la señal  por el Serial**; la predicción se hace en **Python** con un modelo de red neuronal liviano (optimizado) para microcontroladores.



## Requisitos
- Arduino Nano 33 BLE Sense
- Python 3.10
- Arduino IDE 2.x

### Librerias que vamos a utilizar:
-   pyserial
-   numpy
-   wave
-   sounddevice
- PDM (En Arduino IDE)


## 1) Preparar Arduino 
1. Abrí `arduino/comandos_si_no.ino` en Arduino IDE
2. Seleccioná la placa: **Arduino Nano 33 BLE Sense**
3. Seleccioná el puerto (COMx)
4. Subí el sketch

> Importante: cerrá el Serial Monitor del IDE antes de correr Python (Python necesita el puerto).

## 2) Preparar Python (Windows - PowerShell)

### Descarcar los requerimentos :

```powershell
cd python
python -m venv venv
.\venv\Scripts\activate
python -m pip install -r requirements.txt

```
## Ejecutar detección en tiempo real

Editá el puerto en `realtime_si_no.py` PORT="COMx" (elegí el puerto que corresponde) y corré:
```
python realtime_si_no.py
```

## Mejorar la predicción

Para mejorar la predicción necesitamos agregar más muestras de audio al modelo y después entrenarlo.  

## Agregar más audio
Vamos a la carpeta Arduino y compilamos el archivo [comandos_si_no.ino](https://github.com/agustinwec/Proyecto-arduino/blob/main/Roadmaps%20/03Voice-recognition/arduino/comandos_si_no.ino "comandos_si_no.ino") 
Una vez cargado, cerramos el ArduinoIDE y vamos  al archivo [record_word.py](https://github.com/agustinwec/Proyecto-arduino/blob/main/Roadmaps%20/03Voice-recognition/dataset/record_word.py "record_word.py") 

Cambiamos el puerto que corresponda con el del serial
![1.img.png](https://github.com/agustinwec/Proyecto-arduino/blob/main/Roadmaps%20/03Voice-recognition/img/1.img.png?raw=true)

Al ejecutar en el terminal nos va aparecer así
![2.img.png](https://github.com/agustinwec/Proyecto-arduino/blob/main/Roadmaps%20/03Voice-recognition/img/2.img.png?raw=true)
Escribimos "si o no", según cual querés cargar. Apretás enter para seguir cargando el mismos. 

Después de hacer varios audios. Vamos al archivo [prepare_dataset.py](https://github.com/agustinwec/Proyecto-arduino/blob/main/Roadmaps%20/03Voice-recognition/dataset/prepare_dataset.py "prepare_dataset.py") que convierte cada audio en espectrogramas tipo MFCC para después entrenar el modelo de datos.

Una vez que termina de ejecutarse "prepare_dataset.py" nos da un archivo llamado "kws_dataset.npz" donde ya estan preparados los datos que se van a entrenar. 

## Entrenar el modelo
Una vez que los datos estan preparados, vamos a [train_dscnn.py](https://github.com/agustinwec/Proyecto-arduino/blob/main/Roadmaps%20/03Voice-recognition/dataset/train_dscnn.py "train_dscnn.py") 

![3.img.png](https://github.com/agustinwec/Proyecto-arduino/blob/main/Roadmaps%20/03Voice-recognition/img/3.img.png?raw=true)

Los **epochs** son la cantidad de veces que el modelo **recorre todo el conjunto de entrenamiento** durante el aprendizaje

Si ponemos poco epochs, el modelo no llega a aprender bien. 

## Ponemos a prueba la predicción
Una vez entrenado volvemos a ejecutar [realtime_si_no.py](https://github.com/agustinwec/Proyecto-arduino/blob/main/Roadmaps%20/03Voice-recognition/dataset/realtime_si_no.py "realtime_si_no.py") (antes de eso asegurate de estar mandando la señal por el serial con [comandos_si_no.ino](https://github.com/agustinwec/Proyecto-arduino/blob/main/Roadmaps%20/03Voice-recognition/arduino/comandos_si_no.ino "comandos_si_no.ino"). Antes de compilar "realtime_si_no" cerra el ArduinoIDE.

