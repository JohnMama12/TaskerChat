import subprocess
from config import enabled_commands
from blacklist import is_blocked
import re
from commands import divide, multiply,add,subtract, rect_perimeter, rect_diagonal, get_date_time, get_weather_from_lat_long, get_local_weather
def extract_tool_call(text):
    import io
    from contextlib import redirect_stdout
    
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