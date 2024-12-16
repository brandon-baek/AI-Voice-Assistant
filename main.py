import os
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
from cleantext import clean

language = 'en'

# Configure Google Generative AI
genai.configure(api_key='[INSERT API KEY HERE]')

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 0,
    "max_output_tokens": 2048,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    safety_settings=safety_settings,
    generation_config=generation_config,
)

chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "I'm a user and I am human.",
            ],
        },
        {
            "role": "model",
            "parts": [
                "I'm an AI Voice Assistant named Gemini. I was created by Brandon Baek.",
            ],
        }
    ]
)

# Set up the speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init('dummy')
voice = engine.getProperty('voices')[1]
engine.setProperty('voice', voice.id)
name = "Brandon"

def listen_for_wake_word():
    print("Listening for 'brad'...")

    with sr.Microphone() as source:
        while True:
            try:
                audio = r.listen(source, timeout=0.5)
            except Exception:
                pass
            try:
                text = r.recognize_google(audio)
                print(text)
                if "brad" in text.lower() or 'bread' in text.lower():
                    print("Wake word detected.")
                    os.system(f'say "Yes Brandon?"')
                    listen_and_respond()
                    break
            except sr.UnknownValueError:
                pass
            except Exception:
                pass

def listen_and_respond():
    global chat_session
    print("Listening...")

    with sr.Microphone() as source:
        while True:
            audio = r.listen(source, timeout=2)  # Set a timeout to avoid long silence
            try:
                text = r.recognize_google(audio)
                print(f"You said: {text}")
                if not text:
                    continue

                response = chat_session.send_message(text)
                response_text = clean(response.candidates[0].content.parts[0].text.strip(), no_emoji=True)
                print(response_text)

                # Speak the response
                print("speaking")
                os.system(f'say "{response_text}"')  # macOS built-in TTS command

                print('Your Turn')

            except sr.UnknownValueError:
                listen_for_wake_word()
                break

            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                engine.say(f"Could not request results; {e}")
                engine.runAndWait()
                break

listen_for_wake_word()
