from flask import Flask, request, jsonify, send_file
from gtts import gTTS
import os

app = Flask(__name__)

# Ruta para convertir texto a audio
@app.route('/text-to-audio', methods=['POST'])
def text_to_audio():
    try:
        data = request.get_json()
        if not data or 'texto' not in data:
            return jsonify({"error": "No se proporcionó ningún texto para convertir"}), 400

        texto = data['texto']
        audio_file_path = "datosusuario.mp3"  # Guardar con este nombre

        # Convertir texto a audio usando gTTS
        tts = gTTS(text=texto, lang='es')
        tts.save(audio_file_path)

        # Enviar el archivo de audio como respuesta
        return send_file(audio_file_path, as_attachment=True)

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"Ocurrió un error interno en el servidor: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
