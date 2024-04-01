import speech_recognition as sr
from gtts import gTTS
import pygame
from pygame import mixer
from googletrans import Translator

def continuous_speech_to_text(language):
    recognizer = sr.Recognizer()
    translator = Translator(service_urls=['translate.googleapis.com'])

    
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
    
    while True:
        with sr.Microphone() as source:
            print("Say something (or say 'exit' to stop):")
            audio_data = recognizer.listen(source, timeout=15)
            
        try:
            if language == 'english':
                text1 = recognizer.recognize_google(audio_data, language="en-IN")
            elif language == 'malayalam':
                text1 = recognizer.recognize_google(audio_data, language="ml-IN")
                print("Malayalam Text:", text1)
                translation = translator.translate(text1, dest='en')
                if translation:
                    translated_text = translation.text
                    print("Translated Text:", translated_text)
                else:
                    print("Translation failed.")

        
            else:
                print("Invalid language choice.")
                continue

            if "exit" in text1.lower():
                print("Ending speech-to-text.")
                break

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Error with the speech recognition service: {e}")

# Prompt the user to select a language
while True:
    selected_language = input("Select language (English/Malayalam): ").lower()
    if selected_language in ['english', 'malayalam']:
        break
    else:
        print("Invalid input. Please select English or Malayalam.")

# Example usage:
continuous_speech_to_text(selected_language)