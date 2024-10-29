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
    app.run(host='0.0.0.0', port=5000)



#diegosistem09.pythonanywhere.com
#app = Flask(__name__)

# Ruta para convertir texto en audio
@app.route('/text-to-audio', methods=['POST'])
def convert_text_to_audio():
    # Verificar si el texto fue enviado en la solicitud
    if not request.json or 'texto' not in request.json:
        return jsonify({"error": "No se envió ningún texto"}), 400

    texto = request.json['texto']
    try:
        # Convertir el texto a audio usando gTTS
        tts = gTTS(text=texto, lang='es')
        audio_file_path = "output_audio.mp3"
        tts.save(audio_file_path)  # Guardar el archivo de audio

        # Devolver el archivo de audio al cliente
        return send_file(audio_file_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Limpiar el archivo de audio temporal si existe
        if os.path.exists(audio_file_path):
            os.remove(audio_file_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
