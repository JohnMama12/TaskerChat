## **TaskerChat**
<img src="TaskerChat_Logo2.png" width="478.5" height="185">

a Gemma 3 Based AI assistant with Piper TTS that can execute various functions. (Function feature based on [philschmid/gemini-samples/blob/main/examples/gemma-function-calling.ipynb](https://github.com/philschmid/gemini-samples/blob/main/examples/gemma-function-calling.ipynb)

You can ask the Assistant help with:
 - **Mathematical functions:**
	 - Add, Subtract and Multiply any given amount of numbers or decimals.
	 - Divide a fraction
	 - Calculate a rectangle's Diagonal Length
	 - More Mathematical functions will be added in the future
	
 - **General functions:**
	 - Retrieve current date and time
	 - Get both your local weather (IP address based) or the weather of any given location on earth or longitude or latitude (Doesn't work as expected yet)
	 - Run shell commands for you (Note: there are blacklisted commands that are enabled by default which will block the AI from executing dangerous commands, while they can be edited, you risk comprmising your computer by letting it run potentially dangerous commands on accident)
## Setup
TaskerChat Needs Google Generative AI Installed and Piper (Optional for TTS)
	to Install Google Generative AI:
		

    pip install google-genai
 Then, if on Windows set the `GOOGLE_API_KEY` to your Google Cloud  API key (Free version can still work):
 

    
    set GOOGLE_API_KEY=YOUR_API_KEY

to instal Piper it is recommended to directly download it the latest piper version:
https://github.com/rhasspy/piper/releases
Once downloaded extract it to your computer
and set the `PIPER_DIRECTORY` to where you have extracted it:
On Windows:

    set PIPER_DIRECTORY=YOUR_PIPER_PATH
Once that is set go you can download any voice you wish.
You can listen to Voice samples here: https://rhasspy.github.io/piper-samples/ 
by default TaskerChat uses the `en_US-hfc_male` voice.
Once you find a voice you like you can download the model's .onnx from here:
https://github.com/rhasspy/piper/blob/master/VOICES.md
Ensure to also download the model's corresponding .json file, by default it will open a new tab on your browser with the .json file. Copy it and paste it into a new json file, ensure it ends in `.onnx.json` . Once you get both files, copy them to the TaskerChat directory. Then finally change the default voice model:

    voice_path  =  "model_name.onnx"  # set to desired voice model, the .onnx.json file must also exist in the same directory
## Usage
Run by excuting python:
	`python tool_use_gemini_API.py`
By default TTS and the execution of shell commands are disabled, to enable them you can see the help section with `/help` or `/?` to list available commands:

    > /help
    Options:
    /clear - Clears the context
    /clear_screen - Clears the screen without clearing the context
    /allowcommands - Enable or Disable the use of shell commands it's currently set to: True
    /voice - Enable or Disable TTS Voice it's currently set to: True
    /quit - Quits the program

Settings are saved as settings.json once any adjustable setting is changed. If the settings file is deleted the program will fall back to false for both TTS and the running of Shell Commands.
