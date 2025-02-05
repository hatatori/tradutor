import asyncio
from googletrans import Translator
import time
import pyperclip
import keyboard

async def translate_text(text):
    async with Translator() as translator:
        result = await translator.translate(text, dest='en')
        return result.text

while True:
    event = keyboard.read_event() 
    if event.event_type == keyboard.KEY_DOWN:  
        if event.name == "esc": 
            break

    if event.event_type == keyboard.KEY_DOWN:
        if event.name == "*":
            keyboard.press_and_release('backspace')
            time.sleep(0.1)
            keyboard.send("ctrl+a")
            time.sleep(0.1)
            keyboard.send("ctrl+c")
            time.sleep(0.1)
            copied_text = pyperclip.paste()
            translated_text = asyncio.run(translate_text(copied_text))
            keyboard.write(translated_text)
            keyboard.press_and_release('enter')