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


## 1) Preparar Arduino (streaming de audio + LEDs)
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
