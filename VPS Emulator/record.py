import sounddevice as sd
from scipy.io.wavfile import write
from playsound import playsound
import multiprocessing

fs = 44100  # Sample rate
seconds = 3  # Duration of recording

myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
sd.wait()  # Wait until recording is finished
write('output.wav', fs, myrecording) 


playsound("output.wav")
