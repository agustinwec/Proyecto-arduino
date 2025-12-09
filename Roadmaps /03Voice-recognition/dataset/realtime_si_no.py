import serial
import numpy as np
import torch
import librosa
from train_dscnn import DSCNN

# Parámetros
PORT = "COM4"
BAUD = 1000000
SAMPLE_RATE = 16000
WINDOW_SIZE = 16000

SILENCE_RMS = 0.003
device = torch.device("cpu")

# UMBRALES DE DECISIÓN
TH_SI  = 0.70   # exigencia para SI
TH_NO  = 0.60   # exigencia para NO
MARGIN = 0.10   # ventaja mínima

# SUAVIZADO
MIN_STABLE_WINDOWS = 2    # cuántas ventanas iguales antes de cambiar LED
SILENCE_WINDOWS    = 3    # cuántas ventanas de silencio para apagar

model = DSCNN(n_classes=2).to(device)
state = torch.load("dscnn_kws_best.pth", map_location=device)
model.load_state_dict(state)
model.eval()

N_MFCC = 40
N_FFT = 480
HOP_LEN = 160
MAX_FRAMES = 49


def audio_to_mfcc_from_float(y: np.ndarray) -> np.ndarray:
    mfcc = librosa.feature.mfcc(
        y=y,
        sr=SAMPLE_RATE,
        n_mfcc=N_MFCC,
        n_fft=N_FFT,
        hop_length=HOP_LEN,
    )

    if mfcc.shape[1] < MAX_FRAMES:
        pad = MAX_FRAMES - mfcc.shape[1]
        mfcc = np.pad(mfcc, ((0, 0), (0, pad)), mode="constant")
    elif mfcc.shape[1] > MAX_FRAMES:
        mfcc = mfcc[:, :MAX_FRAMES]

    mean = mfcc.mean()
    std = mfcc.std() + 1e-6
    mfcc = (mfcc - mean) / std

    return mfcc[None, None, :, :].astype(np.float32)


def main():
    ser = serial.Serial(PORT, BAUD, timeout=1)
    ser.reset_input_buffer()
    print("Escuchando...")

    buffer = np.zeros(0, dtype=np.int16)

    # Estado para suavizar
    last_instant_label = None   # etiqueta de la ventana anterior ("SI"/"NO")
    stable_count = 0            # cuántas ventanas seguidas con la misma etiqueta
    silence_count = 0           # cuántas ventanas seguidas de silencio
    last_sent_label = None      # última etiqueta enviada al Arduino ("SI"/"NO"/None)

    while True:
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting)
            if len(data) % 2 != 0:
                data = data[:-1]
            samples = np.frombuffer(data, dtype="<i2")
            buffer = np.concatenate([buffer, samples])

        if buffer.shape[0] >= WINDOW_SIZE:
            window_int16 = buffer[-WINDOW_SIZE:]
            buffer = buffer[-WINDOW_SIZE//2:]   # solapamiento 0.5s

            y = window_int16.astype(np.float32) / 32768.0

            # 1) Silencio
            rms = float(np.sqrt(np.mean(y**2)))
            if rms < SILENCE_RMS:
                silence_count += 1
                stable_count = 0
                last_instant_label = None

                # solo apagamos si estuvo silencioso un rato
                if silence_count >= SILENCE_WINDOWS and last_sent_label is not None:
                    ser.write(b'0')
                    last_sent_label = None
                continue
            else:
                silence_count = 0

            # 2) Modelo
            mfcc = audio_to_mfcc_from_float(y)
            x = torch.from_numpy(mfcc).to(device)

            with torch.no_grad():
                logits = model(x)
                probs = torch.softmax(logits, dim=1)[0].cpu().numpy()
                p_no = float(probs[0])
                p_si = float(probs[1])

            # 3) Decisión instantánea 
            instant_label = None   # "SI" / "NO" / None

            if p_si > TH_SI and (p_si - p_no) > MARGIN:
                instant_label = "SI"
            elif p_no > TH_NO and (p_no - p_si) > MARGIN:
                instant_label = "NO"

            if instant_label is None:
                # no suficientemente seguro → no cambiamos nada
                stable_count = 0
                last_instant_label = None
                continue

            # 4) Suavizado: necesitamos MIN_STABLE_WINDOWS iguales
            if instant_label == last_instant_label:
                stable_count += 1
            else:
                stable_count = 1
                last_instant_label = instant_label

            # si no llegamos a suficientes ventanas iguales, no cambiamos LED
            if stable_count < MIN_STABLE_WINDOWS:
                continue

            # 5) Solo enviamos si es distinto de lo último que mandamos
            if instant_label != last_sent_label:
                if instant_label == "SI":
                    ser.write(b'S')
                else:
                    ser.write(b'N')
                print(instant_label)
                last_sent_label = instant_label


if __name__ == "__main__":
    main()
