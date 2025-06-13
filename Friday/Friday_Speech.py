import speech_recognition as sr

# recognizer = sr.Recognizer()
# mic = sr.Microphone()

# with mic as source:
#     audio = recognizer.listen(source)

# output = recognizer.recognize_google(audio)

# print(output)


from gtts import gTTS

def speak(text):
    tts = gTTS(text=text, lang='en', tld='co.uk')  # British accent for Jarvis feel
    tts.save("jarvis_output.mp3")

speak("System check complete. All systems are online sir.")

from playsound import playsound

playsound("jarvis_output.mp3")