const { Client, LocalAuth } = require('whatsapp-web.js');
const FormData = require('form-data');
const fs = require('fs');
const path = require('path');
const qrcode = require('qrcode-terminal');
const axios = require('axios');

const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: false,
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
        ]
    }
});

client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
    console.log("Escanea el código QR con tu WhatsApp.");
});

client.on('authenticated', () => {
    console.log('Sesión autenticada y guardada.');
});

client.on('ready', async () => {
    console.log('El bot está listo');
    await new Promise(resolve => setTimeout(resolve, 8000)); // Espera inicial
});

// Función que maneja la recepción de mensajes
client.on('message', async (message) => {
    if (message.hasMedia) {
        if (message.type === 'audio') {
            // Descargar el archivo de audio
            const media = await message.downloadMedia();
            const filePath = path.join(__dirname, `audio_${message.id.id}.ogg`);

            // Guardar el audio
            fs.writeFileSync(filePath, media.data, 'base64');
            console.log(`Audio guardado como ${filePath}`);

            message.reply('¡Audio recibido y guardado!');

            // Procesar el audio
            try {
                const formData = new FormData();
                formData.append('audio', fs.createReadStream(filePath));

                // Enviar el archivo de audio a Python para convertirlo a texto
                const response = await axios.post('http://127.0.0.1:5000/voice-to-text', formData, {
                    headers: formData.getHeaders()
                });

                console.log('Texto recibido:', response.data.text);

                // Eliminar el archivo de audio después de procesarlo
                fs.unlinkSync(filePath);
            } catch (error) {
                console.error('Error al procesar el audio:', error);
            }
        }
    }
});

client.initialize();