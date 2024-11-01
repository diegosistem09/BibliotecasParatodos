from flask import Flask, request, jsonify, send_file
from gtts import gTTS
import os
import speech_recognition as sr


app = Flask(__name__)

# Ruta para convertir audio en texto
@app.route('/audio-to-text', methods=['POST'])
def convert_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No se envioo ninguun archivo de audio"}), 400

    audio_file = request.files['audio']
    file_path = "temp_audio.wav"
    audio_file.save(file_path)  # Guardar el archivo temporalmente

    # Convertir el audio a texto
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        try:
            # Usar el reconocimiento de Google (por defecto)
            text = recognizer.recognize_google(audio_data, language="es-ES")
        except sr.UnknownValueError:
            text = "No se pudo entender el audio"
        except sr.RequestError:
            text = "Error en la solicitud de reconocimiento"

    os.remove(file_path)  # Eliminar el archivo temporal
    return jsonify({"texto": text})

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=4848)


#diegosistem09.pythonanywhere.com
#app = Flask(__name__)

# Ruta para convertir texto en audio
