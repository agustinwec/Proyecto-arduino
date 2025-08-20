import serial
import time
import pandas as pd
import matplotlib.pyplot as plt
import json
from collections import deque

# ----------------------
# CONFIGURACIÓN
# ----------------------
PORT = "COM3"   # Poner el puerto que coresponda
BAUDRATE = 9600
MAX_POINTS = 200     # Cantidad máxima de puntos a mostrar en el gráfico en vivo

# ----------------------
# INICIALIZAR SERIAL
# ----------------------
ser = serial.Serial(PORT, BAUDRATE, timeout=1)
time.sleep(2)  # Espera a que Arduino resetee

print("Conectado a:", PORT)

tiempo = []
temperatura = []
humedad = []

# Para gráfico en vivo
buffer_tiempo = deque(maxlen=MAX_POINTS)
buffer_temp = deque(maxlen=MAX_POINTS)
buffer_hum = deque(maxlen=MAX_POINTS)

# CONFIGURAR GRAFICO
plt.ion()
fig, ax = plt.subplots()
line_temp, = ax.plot([], [], label="Temperatura (°C)", color="red")
line_hum, = ax.plot([], [], label="Humedad (%)", color="blue")
ax.set_xlabel("Tiempo (ms)")
ax.set_ylabel("Valor")
ax.set_title("Lectura en vivo HTS221")
ax.grid(True)
ax.legend()

# LECTURA EN VIVO
try:
    while True:
        line = ser.readline().decode().strip()
        if line:
            try:
                t, temp, hum = line.split(",")
                t = int(t)
                temp = float(temp)
                hum = float(hum)

                # Guardar en listas completas
                tiempo.append(t)
                temperatura.append(temp)
                humedad.append(hum)

                # Guardar en buffer para gráfico en vivo
                buffer_tiempo.append(t)
                buffer_temp.append(temp)
                buffer_hum.append(hum)

                # Actualizar gráfico
                line_temp.set_data(buffer_tiempo, buffer_temp)
                line_hum.set_data(buffer_tiempo, buffer_hum)
                ax.relim()
                ax.autoscale_view()
                plt.pause(0.01)

            except ValueError:
                continue

except KeyboardInterrupt:
    print("\nCaptura detenida por el usuario")

finally:
    ser.close()
    plt.ioff()
    plt.show()

    # GUARDAR CSV
    df = pd.DataFrame({
        "Tiempo": tiempo,
        "Temperatura": temperatura,
        "Humedad": humedad
    })
    df.to_csv("captura_datos.csv", index=False)
    print("Datos guardados en captura_datos.csv")

    # GENERAR JSON
    resumen = {
        "Temperatura": {
            "min": df["Temperatura"].min(),
            "max": df["Temperatura"].max(),
            "promedio": df["Temperatura"].mean()
        },
        "Humedad": {
            "min": df["Humedad"].min(),
            "max": df["Humedad"].max(),
            "promedio": df["Humedad"].mean()
        },
        "cantidad_muestras": len(df)
    }

    with open("resumen_datos.json", "w") as f:
        json.dump(resumen, f, indent=4)

    print("Resumen guardado en resumen_datos.json")
