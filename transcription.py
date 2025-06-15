import os
import subprocess

from faster_whisper import WhisperModel

url = "https://www.youtube.com/watch?v=A0jA9rB06Zs"
output_name = "audio"

print("Baixando áudio do YouTube...")
subprocess.run(
    ["yt-dlp", "-x", "--audio-format", "mp3", "-o", f"{output_name}.%(ext)s", url]
)

if os.path.exists("audio.mp4"):
    os.rename("audio.mp4", "audio.mp3")

audio_file = f"{output_name}.mp3"

if not os.path.exists(audio_file):
    print(f"Arquivo '{audio_file}' não encontrado.")
    exit(1)

print("Carregando modelo...")
model = WhisperModel("base", device="cpu", compute_type="int8")

print("Transcrevendo áudio...")
segments, info = model.transcribe(audio_file)

print(f"\nIdioma detectado: {info.language}\n")
print("Transcrição:\n")

with open("transcricao.txt", "w", encoding="utf-8") as f:
    for segment in segments:
        linha = f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}\n"
        print(linha, end="")
        f.write(linha)
