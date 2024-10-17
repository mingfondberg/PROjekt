import requests
import tkinter as tk
from tkinter import ttk
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv

# Base URL för FastAPI-servern
API_URL = "http://127.0.0.1:8000/analyze-voice/"

# Funktion för att skicka inspelad ljudfil till FastAPI
def analyze_voice():
    # Filepath till inspelade filen
    file_path = "recording1.wav"
    
    # Skicka POST-anrop till FastAPI med ljudfilen som multipart-form-data
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(API_URL, files=files)
        
    if response.status_code == 200:
        result = response.json()
        mood = result.get("mood")
        playlist = result.get("playlist")
        
        # Uppdatera gränssnittet med humör och länk
        output_window.insert(tk.END, f"Detected Mood: {mood}\nPlaylist: {playlist}\n")
        
        # Ändra bakgrundsfärgen baserat på humöret
        if mood == "calm":
            window.configure(bg='green')
        elif mood == "energetic":
            window.configure(bg='red')
        elif mood == "happy":
            window.configure(bg='blue')
        else:
            window.configure(bg='#5696b8')
    else:
        output_window.insert(tk.END, "Error analyzing voice.\n")

# Funktion för att spela in ljud
def record():
    freq = 44100
    duration = 5
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
    sd.wait()
    write("recording0.wav", freq, recording)
    wv.write("recording1.wav", recording, freq, sampwidth=2)
    analyze_voice()

# Tkinter inställningar för fönstret
window = tk.Tk()
window.title('Emotion Detection')
window.geometry('360x800')
window.configure(bg='#5696b8')

# Outputfält
output_frame = ttk.Frame(master=window)
output_window = tk.Text(master=output_frame, background='#1d4b63')
output_window.pack()
output_frame.pack()

# Inputfält och knappar
input_frame = ttk.Frame(master=window)
button = ttk.Button(master=input_frame, text='Record and Analyze', command=record)
button.pack()
input_frame.pack(pady=10, anchor='center', expand=True)

# Kör Tkinter-mainloop
window.mainloop()