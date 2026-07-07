import time
import requests
import pyperclip
import keyboard

# Endpoint compatível com OpenAI, exposto pelo LM Studio
URL = "http://localhost:1234/v1/chat/completions"
MODEL = "qwen/qwen3-vl-8b"

LANGUAGES = {
    "PT-BR": "Português do Brasil",
    "EN": "Inglês",
}

# Atalho para traduzir uma seleção e apenas imprimir no console
HOTKEY_TRANSLATE_TO_PT = "ctrl+alt+t"

# Tecla que dispara: traduz TUDO que está no campo de texto atual para EN e envia (Enter)
# Atenção: como "*" é um caractere comum, isso dispara sempre que você digitar
# um asterisco em qualquer programa, não só quando quiser traduzir.
TRIGGER_KEY = "*"


def translate(text, language):
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": (
                    f"Traduza o texto abaixo para {language}. "
                    f"Retorne apenas a tradução, sem aspas e sem explicações.\n\n{text}"
                ),
            }
        ],
        "temperature": 0.3,
    }

    response = requests.post(URL, json=payload, timeout=30)
    response.raise_for_status()

    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def get_selected_text():
    """Copia o texto atualmente selecionado e retorna via clipboard."""
    keyboard.send("ctrl+c")
    time.sleep(0.15)
    return pyperclip.paste()


def replace_selected_text(new_text):
    """Digita o novo texto no lugar do texto selecionado (que já foi copiado)."""
    keyboard.write(new_text)


def on_translate_and_print():
    text = get_selected_text()
    if not text.strip():
        return
    try:
        translated = translate(text, LANGUAGES["PT-BR"])
        print(f"\n--- Tradução (PT-BR) ---\n{translated}\n")
    except requests.RequestException as e:
        print(f"[erro] Falha ao traduzir: {e}")


def on_trigger_translate_and_send():
    """Seleciona tudo no campo atual, traduz para EN, substitui e envia (Enter)."""
    keyboard.send("ctrl+a")
    time.sleep(0.1)
    keyboard.send("ctrl+c")
    time.sleep(0.15)

    text = pyperclip.paste()
    
    if not text.strip():
        return

    try:
        translated = translate(text, LANGUAGES["EN"])
        
        keyboard.send("ctrl+a")
        time.sleep(0.1)
        keyboard.press_and_release('backspace')
        
        keyboard.write(translated)



        keyboard.press_and_release("enter")

    except requests.RequestException as e:
        print(f"[erro] Falha ao traduzir: {e}")
        # devolve o texto original já que a tradução falhou
        keyboard.write(text)


def main():
    print("Atalhos ativos:")
    print(f"  {HOTKEY_TRANSLATE_TO_PT}  -> traduz seleção para PT-BR e imprime no console")
    print(f"  '{TRIGGER_KEY}'          -> traduz TUDO no campo atual para EN e envia (Enter)")
    print("Pressione Ctrl+C no terminal para sair.\n")

    keyboard.add_hotkey(HOTKEY_TRANSLATE_TO_PT, on_translate_and_print)
    # suppress=True impede que o "*" seja realmente digitado no campo de texto
    keyboard.add_hotkey(TRIGGER_KEY, on_trigger_translate_and_send, suppress=True)

    keyboard.wait()


if __name__ == "__main__":
    main()
