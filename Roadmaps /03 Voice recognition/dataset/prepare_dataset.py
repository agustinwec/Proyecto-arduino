# prepare_dataset.py
import os
import librosa
import numpy as np
from tqdm import tqdm
import soundfile as sf

SR = 16000
N_MFCC = 40
WIN = 0.030  # 30ms
HOP = 0.010  # 10ms
N_FFT = int(SR * WIN)
HOP_LEN = int(SR * HOP)

def wav_to_mfcc(path):
    x, sr = sf.read(path)
    if sr != SR:
        x = librosa.resample(x.astype(float), sr, SR)
    # ensure mono
    if x.ndim > 1:
        x = x.mean(axis=1)
    mfcc = librosa.feature.mfcc(y=x, sr=SR, n_mfcc=N_MFCC, n_fft=N_FFT, hop_length=HOP_LEN)
    # normalize per-file
    mfcc = (mfcc - np.mean(mfcc)) / (np.std(mfcc) + 1e-9)
    return mfcc.astype(np.float32)  # shape: (n_mfcc, frames)

def pad_or_trim(mfcc, max_frames=49):
    # queremos formato fijo: (N_MFCC, max_frames)
    if mfcc.shape[1] > max_frames:
        return mfcc[:, :max_frames]
    out = np.zeros((N_MFCC, max_frames), dtype=np.float32)
    out[:, :mfcc.shape[1]] = mfcc
    return out

def build_dataset(root='.', max_frames=49):
    # Solo tomamos como clases las carpetas 'no' y 'si'
    classes = [d for d in sorted(os.listdir(root))
               if os.path.isdir(os.path.join(root, d)) and d in ('no', 'si')]
    X = []
    Y = []
    label_map = {c: i for i, c in enumerate(classes)}
    for c in classes:
        folder = os.path.join(root,c)
        for f in os.listdir(folder):
            if not f.lower().endswith('.wav'): continue
            p = os.path.join(folder,f)
            mfcc = wav_to_mfcc(p)
            mfcc = pad_or_trim(mfcc, max_frames)
            X.append(mfcc)
            Y.append(label_map[c])
    X = np.stack(X)   # shape (N, N_MFCC, max_frames)
    Y = np.array(Y, dtype=np.int64)
    # Reorder to (N, 1, N_MFCC, max_frames) or to flattened? we'll use (N, 1, N_MFCC, frames)
    X = X[:, np.newaxis, :, :]
    return X, Y, classes

if __name__=='__main__':
    X, Y, classes = build_dataset('.', max_frames=49)
    print('classes:', classes)
    print('X shape', X.shape)
    np.savez('kws_dataset.npz', X=X, Y=Y, classes=classes)
    print('Saved kws_dataset.npz')
