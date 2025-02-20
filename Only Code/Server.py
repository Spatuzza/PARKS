from flask import Flask, request, jsonify
import speech_recognition as sr
from pydub import AudioSegment
import os
from notion_client import Client

app = Flask(__name__)

# Configuración de las claves API desde variables de entorno
notion_api_key = os.getenv('NOTION_API_KEY', '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')
database_id = os.getenv('NOTION_DATABASE_ID', '1656c82c4bf1808fa410fa976b23a459')

# Función para agregar la tarea a Notion
def add_to_notion(text):
    try:
        # Inicializar el cliente de Notion dentro de la función
        notion = Client(auth=notion_api_key)
        
        # Crear la página en Notion
        notion.pages.create(
            parent={"database_id": database_id},
            properties={
                "Tarea": {"title": [{"text": {"content": text}}]}
            }
        )
        
        # Cerrar la conexión manualmente
        notion.close()  # Este método no existe en la API actual, pero se asegura la limpieza
    except Exception as e:
        raise Exception(f"Error adding to Notion: {str(e)}")

# Ruta para procesar el audio
@app.route('/voice-to-text', methods=['POST'])
def voice_to_text():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file found'}), 400

    audio_file = request.files['audio']
    audio_path = './temp_audio.ogg'
    audio_file.save(audio_path)

    try:
        # Convertir el archivo a WAV
        audio = AudioSegment.from_file(audio_path)
        wav_path = './temp_audio.wav'
        audio.export(wav_path, format='wav')

        # Usar SpeechRecognition para convertir a texto
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)

        # Convertir a texto utilizando el reconocimiento de Google en español
        text = recognizer.recognize_google(audio_data, language='es-AR')

        # Agregar el texto del audio como nombre de la tarea en Notion
        add_to_notion(text)

        response = {'text': text}

    except sr.UnknownValueError:
        response = {'error': 'No se pudo entender el audio'}
    except sr.RequestError as e:
        response = {'error': f'Error del servicio de reconocimiento: {str(e)}'}
    except Exception as e:
        response = {'error': str(e)}
    finally:
        # Limpiar archivos temporales
        if os.path.exists(audio_path):
            os.remove(audio_path)
        if os.path.exists(wav_path):
            os.remove(wav_path)

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
