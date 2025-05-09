import os
import json
enabled_commands = False
use_voice = False
can_use_tts = True
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
def save_json(use_voice,enabled_commands):
    settings_file = {
    "voice":use_voice,
    "allowcommands":enabled_commands,

}
    json_object = json.dumps(settings_file, indent=4)
 
# Writing to sample.json
    with open("settings.json", "w") as outfile:
        outfile.write(json_object)   
try:
    with open('default_prompt.txt', 'r') as file:
        system_instruct = file.read()
except Exception as e:
    print(f"Default prompt could not be read: {e}")
    quit()
    