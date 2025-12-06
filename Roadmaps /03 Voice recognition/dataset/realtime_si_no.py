import serial
import numpy as np
import torch
import librosa
from train_dscnn import DSCNN

# Parámetros
PORT = "COM3"          # cambiá si tu Arduino está en otro puerto
BAUD = 1000000
SAMPLE_RATE = 16000
WINDOW_SIZE = 16000    # 1 segundo

SILENCE_RMS = 0.01     # umbral de silencio (ajustable)
CONF_THRESH = 0.02     # umbral de confianza (ajustable)

device = torch.device("cpu")
model = DSCNN(n_classes=2).to(device)
state = torch.load("dscnn_kws.pth", map_location=device)
model.load_state_dict(state)
model.eval()

CLASSES = ["no", "si"]

def audio_to_mfcc_from_float(y: np.ndarray) -> np.ndarray:
    
    mfcc = librosa.feature.mfcc(
        y=y,
        sr=SAMPLE_RATE,
        n_mfcc=40,
        n_fft=640,
        hop_length=320,
    )
    # Ajustar a 49 frames
    if mfcc.shape[1] < 49:
        pad = 49 - mfcc.shape[1]
        mfcc = np.pad(mfcc, ((0, 0), (0, pad)), mode="constant")
    elif mfcc.shape[1] > 49:
        mfcc = mfcc[:, :49]


    mean = mfcc.mean()
    std = mfcc.std() + 1e-6
    mfcc = (mfcc - mean) / std

    mfcc = mfcc[None, None, :, :].astype(np.float32)  # (1,1,40,49)
    return mfcc

def main():
    ser = serial.Serial(PORT, BAUD, timeout=1)
    ser.reset_input_buffer()

    print(f"Escuchando en {PORT} @ {BAUD} ...")

    buffer = np.zeros(0, dtype=np.int16)

    while True:
        # Leer lo que haya disponible del Arduino
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting)
            if len(data) % 2 != 0:
                data = data[:-1]
            samples = np.frombuffer(data, dtype="<i2")
            buffer = np.concatenate([buffer, samples])

        # Si tenemos al menos 1 segundo
        if buffer.shape[0] >= WINDOW_SIZE:
            window_int16 = buffer[-WINDOW_SIZE:]    # últimas 16000 muestras
            buffer = np.zeros(0, dtype=np.int16)    # limpiamos

            # Pasar a float en [-1,1]
            y = window_int16.astype(np.float32) / 32768.0

            # 1) Detectar SILENCIO
            rms = float(np.sqrt(np.mean(y**2)))
            if rms < SILENCE_RMS:
                # Silencio: no mandamos predicción, apagamos LEDs
                
                ser.write(b'0')  # comando para "apagar" en Arduino
                continue

            # 2) MFCC + modelo
            mfcc = audio_to_mfcc_from_float(y)
            x = torch.from_numpy(mfcc).to(device)

            with torch.no_grad():
                logits = model(x)
                probs = torch.softmax(logits, dim=1)[0].cpu().numpy()
                pred_idx = int(np.argmax(probs))
                max_prob = float(probs[pred_idx])
                label = CLASSES[pred_idx]

            # 3) Filtrar por confianza
            if max_prob < CONF_THRESH:
                print(f"Inseguro: {label} (p={max_prob:.2f}, rms={rms:.4f}) → ignorado")
                ser.write(b'0')  # no confiamos, apagamos LEDs
                continue

            # 4) Predicción válida → mandar comando al Arduino
            print(f"Predicción: {label} ") #(p={max_prob:.2f}, rms={rms:.4f})

            if label == "si":
                ser.write(b'S')   # "si"
            else:
                ser.write(b'N')   # "no"

if __name__ == "__main__":
    main()
