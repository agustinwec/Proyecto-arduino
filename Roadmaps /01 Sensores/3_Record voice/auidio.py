import serial
import wave
import numpy as np

# Configuración
COM_PORT = 'COM3'   # Cambiar por el puerto real
BAUD_RATE = 115200
SAMPLE_RATE = 16000
DURATION_SECONDS = 10
FILENAME = 'grabacion.wav'

# Abrir puerto Serial
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

# Convertir a numpy array
audio_np = np.array(audio, dtype=np.int16)

# Guardar como WAV
with wave.open(FILENAME, 'wb') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(audio_np.tobytes())

print(f"📂 Archivo guardado como: {FILENAME}")

# Reproducir audio (opcional)
import sounddevice as sd
sd.play(audio_np, SAMPLE_RATE)
sd.wait()
print("🔊 Reproducción terminada.")
