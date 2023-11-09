# importamos librerias para reconocer mediante el microfono lo que le pedimos y convertirlo a texto
import speech_recognition as sr
import subprocess as sub
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import cv2
import smtplib

# se crea la variable con el nombre de la asistente que recibirá los comandos
name = "Osiris"

# esta variable comenzará a reconocer lo que le decimos
listener = sr.Recognizer()

# iniciamos la librería
engine = pyttsx3.init()

# mediante estas variables escogeremos el tipo de voz de la asistente
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)
engine.setProperty('rate', 145)

# se listan los sitios donde ingresa la asistente
sites = {
    'google': 'google.com',
    'youtube': 'youtube.com',
    'facebook': 'facebook.com'
}

# definimos esta función para que la asistente hable
def talk(text):
    engine.say(text)
    engine.runAndWait()

# mediante esta función utilizará el micrófono escuchará y reconocerá los comandos
def listen():
    try:
        with sr.Microphone() as source:
            print("Recibiendo comando....")
            # aquí se le solicita que reconozca desde la fuente y utilice los servicios de google
            pc = listener.listen(source)
            rec = listener.recognize_google(pc, language="es")
            rec = rec.lower()
            if name in rec:
                rec = rec.replace(name, '')
    except:
        pass
    return rec

# función principal donde estarán las órdenes que recibirá mediante palabras clave
def run_osiris():
    while True:
        rec = listen()
        # mediante este ciclo al decir la palabra clave ingresará a youtube a reproducir una canción
        if 'reproduce' in rec:
            music = rec.replace('reproduce', '')
            print("Reproduciendo " + music)
            talk("Reproduciendo" + music)
            pywhatkit.playonyt(music)
        # si decimos esta palabra clave ingresa a wikipedia en español y con una cantidad de oraciones
        elif 'busca' in rec:
            search = rec.replace('busca', '')
            wikipedia.set_lang("es")
            wiki = wikipedia.summary(search, 2)
            print(search + ": " + wiki)
            talk(wiki)
        # si decimos esta palabra clave nos dirá la hora actual según nuestro pc en tiempo real
        elif 'hora' in rec:
            hora = rec.replace(' ', ' ')
            hora = datetime.datetime.now().strftime('%H:%M')
            talk("La hora actual es" + hora)
        # si decimos esta palabra clave ingresará a google y mediante el subproceso llamará a nuestro sitio
        elif 'abre' in rec:
            for site in sites:
                if site in rec:
                    sub.call(f'start chrome.exe {sites[site]}', shell=True)
                    talk(f'Abriendo {site}')
        # si decimos esta palabra clave llamará la librería por la cual habrá acceso a nuestra cámara y tomará la foto
        elif 'foto' in rec:
            talk("comando recibido")
            cap = cv2.VideoCapture(0)
            talk("buscando camara")
            # se establece dimensiones de la imagen
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)
            talk("alistando camara")
            talk("preparese para la foto")
            talk("listo para la foto")
            
            # espera un momento para que la cámara se estabilice
            cv2.waitKey(1000)
            
            # realiza captura de la imagen
            ret, frame = cap.read()
            
            if ret:
                talk("foto lista")
                # guarda la imagen en el archivo mediante la ruta
                cv2.imwrite('C:/Users/heidy/Desktop/Python/rostro.jpg', frame)
            else:
                talk("Error al capturar la foto")
            
            cap.release()
        # si decimos esta palabra clave tomará el mensaje que escribimos, y tendrá un asunto
        elif 'correo' in rec:
            message = 'hola como esta'
            subject = 'correo de prueba'
            message = 'Subject: {}\n\n{}'.format(subject, message)
            # mediante la librería se establecerá conexión y el puerto de gmail
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            # se inicializa sesión en el servidor escribiendo el correo y la contraseña para aplicaciones
            server.login('streamingsarestey@gmail.com', 'jlvb fuij gmhe ntix')
            # mediante este comando se envía el correo
            server.sendmail('streamingsarestey@gmail.com', 'heidyj94@gmail.com', message)
            # mediante este se desconecta del servidor
            server.quit()
            print("correo enviado exitosamente")
        # si decimos esta palabra clave sale del ciclo y termina el proceso
        elif 'termina' in rec:
            talk('Buen día, fue un placer ayudarte')
            break

if __name__ == '__main__':
    run_osiris()
