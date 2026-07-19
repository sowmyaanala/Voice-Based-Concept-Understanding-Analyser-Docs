import whisper

model = whisper.load_model("base")

def speech_to_text(audio_path):
    result = model.transcribe(audio_path)
    return result["text"]

if __name__ == "__main__":
    audio_file = "sample.wav"
    text = speech_to_text(audio_file)
    print(text)