from playsound import playsound
from flask import Flask, json, request,jsonify,Response
from flask_cors import CORS, cross_origin
import sounddevice as sd
from scipy.io.wavfile import write
import multiprocessing
import socket
import pyaudio
import wave
import time
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
p = multiprocessing.Process(target=playsound, args=("Noise.wav",))

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 4
WAVE_OUTPUT_FILENAME = "server_output.wav"
WIDTH = 2
frames = []

p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)


HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)


@app.route('/on',methods = ['GET'])
def tunon():
    #playsound("Noise.wav")
    p.start()
    return jsonify({"played":"true"})

@app.route('/off',methods = ['GET'])
def turnoff():
    #playsound("Noise.wav")
    p.terminate()
    return jsonify({"played":"false"})

@app.route('/sq',methods = ['GET'])
def sq():
    playsound("Starting.wav")
    return jsonify({"played":"true"})

@app.route('/chat',methods = ['GET'])
def send():
    data = conn.recv(1024)

    i=1
    while data != '':
        stream.write(data)
        data = conn.recv(1024)
        i=i+1
        print(i)
        frames.append(data)
        
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    stream.stop_stream()
    stream.close()
    p.terminate()
    conn.close()
    return jsonify({"chat":"true"})

if __name__ == '__main__':
    app.run(host="0.0.0.0")

