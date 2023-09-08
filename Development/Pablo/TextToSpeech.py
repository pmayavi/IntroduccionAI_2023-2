import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty("voices")
for voice in voices:
    print(voice, voice.id)
    engine.setProperty("voice", voice.id)
    print(voice.id)
    print(voice.id)
    print(voice.id)
    engine.say("Hola perras sapas")
    engine.runAndWait()
    engine.stop()

# HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0
