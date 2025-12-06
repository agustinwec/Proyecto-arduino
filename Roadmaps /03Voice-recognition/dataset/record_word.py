import os
import sys
import time
import wave
import serial
import numpy as np
from glob import glob

# ======== CONFIGURACIÓN ========
COM_PORT = 'COM3'          # CAMBIAR si tu Arduino está en otro puerto
BAUD_RATE = 115200
SAMPLE_RATE = 16000        # 16 kHz
DURATION_SECONDS = 1.0     # duración de cada clip en segundos
CHANNELS = 1
SAMPLE_WIDTH = 2           # 16 bits = 2 bytes

# ===============================

def next_index(folder, label):
    os.makedirs(folder, exist_ok=True)
    pattern = os.path.join(folder, f"{label}_*.wav")
    files = glob(pattern)
    if not files:
        return 1
    nums = []
    for f in files:
        base = os.path.basename(f)
        # label_XXX.wav
        try:
            n = int(base.replace(label + "_", "").replace(".wav", ""))
            nums.append(n)
        except ValueError:
            pass
    return max(nums) + 1 if nums else 1


def record_clip(ser, num_samples):
    """Lee num_samples muestras int16 desde el puerto serie."""
    bytes_needed = num_samples * SAMPLE_WIDTH
    data = bytearray()

    while len(data) < bytes_needed:
        chunk = ser.read(bytes_needed - len(data))
        if not chunk:
            # pequeño descanso si no llega nada
            time.sleep(0.001)
            continue
        data.extend(chunk)

    audio = np.frombuffer(data, dtype='<i2')  # little-endian int16
    return audio


def main():
    # 1) elegir etiqueta
    if len(sys.argv) >= 2:
        label = sys.argv[1].strip().lower()
    else:
        label = input("Palabra (si / no): ").strip().lower()

    if label not in ("si", "no"):
        print("Etiqueta inválida. Usa 'si' o 'no'.")
        sys.exit(1)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    folder = os.path.join(base_dir, label)

    # 2) abrir serie
    print(f"Abriendo puerto serie {COM_PORT} a {BAUD_RATE}...")
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # tiempo para que Arduino reseteé
    ser.reset_input_buffer()
    print("✅ Puerto abierto.")

    num_samples = int(SAMPLE_RATE * DURATION_SECONDS)

    try:
        while True:
            idx = next_index(folder, label)
            filename = os.path.join(folder, f"{label}_{idx:03d}.wav")

            cmd = input(f"\n[Enter] para grabar '{label}_{idx:03d}.wav' | [q] para salir: ").strip().lower()
            if cmd == 'q':
                print("Saliendo.")
                break

            print("🎙️  Hablá ahora...")
            ser.reset_input_buffer()
            audio = record_clip(ser, num_samples)
            print("✅ Grabación terminada. Guardando WAV...")

            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(SAMPLE_WIDTH)
                wf.setframerate(SAMPLE_RATE)
                wf.writeframes(audio.tobytes())

            print(f"📂 Guardado como: {filename}")

    finally:
        ser.close()
        print("🔌 Puerto serie cerrado.")


if __name__ == "__main__":
    main()
