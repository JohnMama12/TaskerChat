import google.generativeai as genai
import os
import re
import time
import os.path
import json
from tts import speak
import blacklist
from tools import extract_tool_call
import commands
from config import enabled_commands, use_voice, can_use_tts,system_instruct, save_json
model = genai.GenerativeModel('gemma-3-27b-it')
chat = model.start_chat()
print("Info: type /? or /help for help.")
while True:
    user_input = input("> ")
    if user_input == "/?" or user_input == "/help":
        print(f"Options:\n/clear - Clears the context\n/clear_screen - Clears the screen without clearing the context\n/allowcommands - Enable or Disable the use of shell commands it's currently set to: {enabled_commands}\n/voice - Enable or Disable TTS Voice it's currently set to: {use_voice}\n/quit - Quits the program")
    elif user_input == "/clear":
        print("clear chat")
        chat = model.start_chat()
        try:
            os.system('cls')
        except Exception:
            os.system('clear')
    elif user_input == "/clear_screen":
        try:
            os.system('cls')
        except Exception:
            os.system('clear')
    elif user_input == "/quit":
        quit()
    elif user_input.startswith("/allowcommands"):
        print("info: detected enable_commands")
        if "true" in user_input.lower():
            print("Warn: Enabled Commands")
            enabled_commands = True
            
            save_json(use_voice,enabled_commands)
        elif "false" in user_input.lower():
            print("Warn: Dsisabled Commands")
            enabled_commands = False
            save_json(use_voice,enabled_commands)

    elif user_input.startswith("/voice"):
        print("info: detected voice")
        if "true" in user_input.lower():
            print("Warn: Enabled Voice")
            use_voice = True
            save_json(use_voice,enabled_commands)
        elif "false" in user_input.lower():
            print("Warn: Dsisabled Commands")
            use_voice = False
            save_json(use_voice,enabled_commands)
    else:
        #print("debug: not using command")
        try:
            response = chat.send_message(f"<start_of_turn>system\n{system_instruct}\n<start_of_turn>user\n{user_input}\n<start_of_turn>model\n")
            is_using = cleaned_response = re.sub(r'```.*?```', '', response.text, flags=re.DOTALL)
            print(cleaned_response)
            
            if use_voice == True and can_use_tts == True:
                speak(cleaned_response)
        except Exception as e:
            #print(e)

            print("Error! There was an Error sending the message. Please check your API Key or max quota was reached. wait a couple seconds before retrying.")
            continue
        command = extract_tool_call(response.text)
        #print(f"(debug) command: {command}")
        if not command == None:
            #print("debug: giving the AI the result")
            time.sleep(2)
            print("Warn: Waiting 2 seconds to prevent API Overload!")
            seconds = 0
            while True:

                try:
                    time.sleep(seconds)
                    response = chat.send_message(f"<start_of_turn>system\n{system_instruct}\n<start_of_turn>user\n{command}\n<start_of_turn>model\n")
                    print(response.text)
                    if use_voice == True and can_use_tts == True:
                        speak(response.text)
                        break
                    break
                except Exception as e:
                    #print(e)
                    
                    print(f"Error! There was an Error sending the message. retrying in {seconds} seconds.")
                    seconds +=3
                    continue
