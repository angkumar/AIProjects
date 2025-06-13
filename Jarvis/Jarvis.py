# pip3 install requests
import requests
from bs4 import BeautifulSoup
import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError

import speech_recognition as sr

recognizer = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
    audio = recognizer.listen(source)

output = recognizer.recognize_google(audio)


print(output)

query = output
results = wikipedia.search(query)

import pyttsx3

def get_summary(results):
    for result in results:
        try:
            summary = wikipedia.summary(result, sentences=6)
            return summary
        except DisambiguationError as e:
            try:
                summary = wikipedia.summary(e.options[0], sentences=6)
                return summary
            except Exception:
                continue
        except PageError:
            continue
    return "aye bruh my fault cuh i couldn't find anything that u want gng mb"

summary = get_summary(results)
print(summary)

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)  # Adjust speed
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()

speak(summary)