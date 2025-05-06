import google.generativeai as genai
import os
import sys
import re
import math
import time
from playaudio import playaudio
import subprocess
import os.path
import datetime
import json
import requests
import warnings
BLACKLIST = [ # Change at your own risk, or  the AI could cause irreversable damage to your computer.
    r"rm\s+-rf\s+/?",
    r":\(\)\s*{\s*:.*:.*&\s*};:",
    r"mkfs",
    r"dd\s+if=",
    r"shutdown",
    r"reboot",
    r"halt",
    r"poweroff",
    r"chmod\s+000",
    r"chown\s+.*nobody",
    r"mv\s+/bin",
    r"yes\s+>",
    r"eval\s+",
    r"(wget|curl).*\|.*sh",
    r"kill\s+-9\s+-1",
    r"pkill",
    r"mount\s+/dev",

    r"del\s+/f\s+/q",
    r"rd\s+/s\s+/q",
    r"format\s+c:",
    r"reg\s+delete",
    r"cipher\s+/w:",
    r"vssadmin",
    r"net\s+user.*\*",
    r"net\s+stop",
    r"taskkill",
    r"powershell\s+.*(remove|invoke)",
    r"bcdedit",
    r"echo\s+y\|cacls",
    r"echo\s+test"
]
enabled_commands = False
use_voice = False
can_use_tts = True
voice_path = "en_US-hfc_male-medium.onnx" # set to desired voice model, the .onnx.json file must also exist in the same directory 
try:
    piper_dir = os.environ['PIPER_DIRECTORY']
except Exception as e:
    can_use_tts = False
    print("Warn: Piper is not detected. TTS Temporarily disabled.. Please ensure PIPER_DIRECTORY is set in your enviorment variables.")
if not os.path.isfile("settings.json"):
    enabled_commands = False
    use_voice = False
    print("Settings file not created yet. Loaded default settings.")
else:
    try:
        with open('settings.json', 'r') as file:
            current_setting_file = json.load(file)
            enabled_commands = current_setting_file["allowcommands"]
            use_voice = current_setting_file["voice"]
            print("Info: Loaded settings succesfully.")
    except Exception:
        print("Error: Could not open settings.json or set the settings file: Fallback to default settings.")
        enabled_commands = False
        use_voice = False
def save_json():
    settings_file = {
    "voice":use_voice,
    "allowcommands":enabled_commands,

}
    json_object = json.dumps(settings_file, indent=4)
 
# Writing to sample.json
    with open("settings.json", "w") as outfile:
        outfile.write(json_object)   




def is_blocked(command):
    return any(re.search(p, command, re.IGNORECASE) for p in BLACKLIST)

def extract_tool_call(text):
    import io
    from contextlib import redirect_stdout
    def add(*args):
        total = 0
        for arg in args:
            total += arg
        return total
    
    def divide(*a,b):
        return round(a/b)
        
    def multiply(*args):
        total = 1
        for arg in args:
            total *= arg
        return total
    def subtract(*args):
        total = 0
        for arg in args:
            total *= arg
        return total
    def rect_perimeter(l,w):
        return (2 * (l+w))
    def rect_diagonal(l,w):
        return math.sqrt((math.pow(l,2) + math.pow(w,2)))
    #print(f"(debug) text: {text}")
    def get_date_time():
        x = datetime.datetime.now()
        return x
    def get_weather_from_lat_long(lat,lon):
        weather = requests.post(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,rain,showers&timezone=auto")
        return weather.json
    def get_local_weather():
        try:
            ip_response = requests.get("https://api.ipify.org/?format=plaintext")
            ip = ip_response.text.strip()
            #print(f"Public IP: {ip}")
            lat_long = requests.get(f"http://ip-api.com/json/{ip}")
            #print(f"Latitude and Longitude: {lat_long}")
            location = lat_long.json()
            lat = location["lat"]
            lon = location["lon"]
            weather = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,rain,showers&timezone=auto")
            #print(f"Weather: {weather}")

            return weather.json()
        except Exception as e:
            #print(e)
            return e


    def run_command(command):
        if enabled_commands == True and is_blocked(command) == False:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            return result
        elif enabled_commands == False:
            return "For Security reasons running commands are OFF."
        elif is_blocked(command) == True:
            return f"The command: {command} was blacklisted due to potential malicious intent"
    pattern = r"```tool_input\s*(.*?)\s*```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        code = match.group(1).strip()
        # Capture stdout in a string buffer
        f = io.StringIO()
        with redirect_stdout(f):
            try:
                result = eval(code)
                print(f"result: {result}")
            except Exception as e:
                print(f"error: {e}")
                return str(e)
            else:
                output = f.getvalue()
                r = result if output == '' else output
                return f'```tool_output\n{str(r).strip()}\n```'''
def speak(text):
    process = subprocess.run(
        [piper_dir+r'/piper.exe', '--model', voice_path, '--output_file', 'out2.wav'],
        input=text.encode('utf-8'),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    if process.returncode != 0:
        print(f"Error: Could not speak. Ensure both .onnx and config file is present.")
        
    else:
        #print("Speech synthesis completed successfully.")
        sound = playaudio("out2.wav")
        #print(sound)

#genai.configure(api_key="") # Use default API key
try:
    with open('default_prompt.txt', 'r') as file:
        system_instruct = file.read()
except Exception as e:
    print(f"Default prompt could not be read: {e}")
    quit()
    
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
            save_json()
        elif "false" in user_input.lower():
            print("Warn: Dsisabled Commands")
            enabled_commands = False
            save_json()
    elif user_input.startswith("/voice"):
        print("info: detected voice")
        if "true" in user_input.lower():
            print("Warn: Enabled Voice")
            use_voice = True
            save_json()
        elif "false" in user_input.lower():
            print("Warn: Dsisabled Commands")
            use_voice = False
            save_json()
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
        #sprint(f"(debug) command: {command}")
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
                except Exception as e:
                    #print(e)
                    
                    print(f"Error! There was an Error sending the message. retrying in {seconds} seconds.")
                    seconds +=3
                    continue
