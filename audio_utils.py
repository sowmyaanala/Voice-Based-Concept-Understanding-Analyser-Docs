import librosa
import numpy as np

def analyze_audio(audio_path):
    y, sr = librosa.load(audio_path)

    duration = librosa.get_duration(y=y, sr=sr)
    rms_energy = np.mean(librosa.feature.rms(y=y))
    pauses = np.sum(np.abs(y) < 0.01)
    pause_ratio = pauses / len(y)

    return {
        "duration": duration,
        "rms_energy": float(rms_energy),
        "pause_ratio": float(pause_ratio)
    }