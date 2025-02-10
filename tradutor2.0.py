import time
import pyperclip
import keyboard

from google import genai

languages = {
    "PT-BR": "Português do Brasil",
    "EN": "Inglês",
    "ES": "Espanhol",
    "FR": "Francês",
    "DE": "Alemão",
    "IT": "Italiano",
    "ZH-CN": "Chinês (Simplificado)",
    "JA": "Japonês",
    "RU": "Russo",
    "AR": "Árabe",
    "KO": "Coreano",
    "HI": "Hindi",
    "BN": "Bengali",
    "PA": "Panjabi",
    "UR": "Urdu",
    "ID": "Indonésio",
    "SW": "Suaíli",
    "TR": "Turco",
    "VI": "Vietnamita",
    "FA": "Persa",
    "TA": "Tâmil",
    "MR": "Marata",
    "TE": "Telugu",
    "TH": "Tailandês",
    "GU": "Guzerate",
    "PL": "Polonês",
    "UK": "Ucraniano",
    "MY": "Birmanês",
    "ML": "Malaiala",
    "AM": "Amárico",
    "YO": "Iorubá"
}

def translate(text, language='en'):
    # create your api here
    # https://ai.google.dev/gemini-api/docs/quickstart?hl=pt-br&lang=python
    apiKey = 'api_key'
    client = genai.Client(api_key=apiKey)
    response = client.models.generate_content(
        model="gemini-1.5-flash", contents=f"traduza isso para a linguagem {language} sem aspas, não escreva nada mais além disso: "+text
    )
    return response.text


def main():
    while True:
        event = keyboard.read_event() 

        if event.event_type == keyboard.KEY_DOWN:
            
            if event.name == "/":
                keyboard.send("ctrl+c")
                time.sleep(0.1)
                copied_text = pyperclip.paste()
                translated_text = translate(copied_text, 'pt_br')
                print(translated_text)
            
            if event.name == "*":
                keyboard.press_and_release('backspace')
                time.sleep(0.1)
                keyboard.send("ctrl+a")
                time.sleep(0.1)
                keyboard.send("ctrl+c")
                time.sleep(0.1)
                copied_text = pyperclip.paste()
                translated_text = translate(copied_text, languages['EN'])
                keyboard.write(translated_text)
                keyboard.press_and_release('enter')

if __name__ == "__main__":
    main()