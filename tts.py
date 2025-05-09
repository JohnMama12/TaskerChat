import subprocess
from config import piper_dir
from playaudio import playaudio
voice_path = "en_US-hfc_male-medium.onnx" # set to desired voice model, the .onnx.json file must also exist in the same directory 
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