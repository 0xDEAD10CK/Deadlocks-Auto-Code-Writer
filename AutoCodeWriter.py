from openai import OpenAI
import os
import pyautogui
import time
import random
import subprocess
import re
from pywinauto import Application
from stopwatch import Stopwatch
from dotenv import load_env

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def remove_first_line(text):
    # Removes the first line from the text
    lines = text.split('\n')
    if len(lines) > 2:
        return '\n'.join(lines[1:])
    return ''

def extract_code_blocks(text):
    # Splitting by triple backticks or other code block delimiters
    return [block.strip() for block in text.split('```') if block.strip()]

def navigate_up(levels):
    for _ in range(levels):
        pyautogui.hotkey('alt', 'up')  # Use Alt+Up to navigate up one directory

def create_workspace(directory):

    # Create the directory
    try:
        subprocess.run(["mkdir", directory], shell=True, check=True)
        print(f"Directory: {directory} created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create directory: {e}")
        exit(1)

    # Wait a bit before opening the directory in VS Code
    time.sleep(4)

    # Open the directory in Visual Studio Code
    code_path = r"C:\Program Files\Microsoft VS Code\Code.exe"  # Adjust path if necessary
    try:
        subprocess.Popen([code_path, directory])
        print(f"Visual Studio Code in {directory} opened successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to open Visual Studio Code: {e}")
        exit(1)

    time.sleep(6)
    pyautogui.press('enter')
    
def focus_vscode(directory):
    # Using Pywinauto to bring VSCode into focus
    app = Application(backend='uia').connect(title_re=f".*{directory} - Visual Studio Code.*")
    app.window(title_re=f".*{directory} - Visual Studio Code.*").set_focus()
    print("Focused on Visual Studio Code.")
    
def send_request():
    directory = f"Application-{random.randint(10000, 99999)}"
    file_content = ""
    depth = ""
    selector = input("Create Workspace? (y/n): ")

    if selector == 'y':
        create_workspace(directory)

    focus_vscode(directory)
    time.sleep(2)
    pyautogui.hotkey('ctrl', 'n')
    
    osName = os.name
    if osName == "nt":                              
        osName = "Windows"

    with open("request.txt", 'r') as file:
        file_content = file.read()

    print(file_content)

    stopwatch = Stopwatch(3)
    completion = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[{"role": "system", "content": "You are a helpful assistant that will only return code blocks in a given language. The first line is the name of the file. The last line of each block is always a disclaimer this code was written by AI"},
                {"role": "user", "content": file_content}]
    )

    stopwatch.stop()
    print(str(stopwatch))
    
    text = completion.choices[0].message.content

    print("--------------------------------")
    print("GPT RESPONSE")
    print(text)

    code_blocks = extract_code_blocks(text)

    last_saved_directory = directory
    
    for idx1, code_block in enumerate(code_blocks):
        print(code_block)
        filename = ""
        # Remove delimiters and unnecessary newlines
        processed_code_block = remove_first_line(code_block)
        
        # Write each line of the code block using pyautogui
        for idx2, line in enumerate(processed_code_block.split('\n')):
            if idx2 == 0:
                # Get the name of the file from the first line.
                # If the name is commented, remove comment characters.
                line = re.sub(r'^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$', '', line)

                print("LINE: " + line)

                line = line.replace('/', os.sep)  # Replace '/' with the OS-specific separator

                print("REPLACE LINE: " + line)

                # Set the full path before any string manipulation
                full_path = os.path.join(directory, line)
                
                filename = line

                print("FILENAME: " + filename)

                # Create directories if necessary
                directory_path = os.path.dirname(full_path)
                print("DIRECTORY PATH: " + directory_path)

                # Calculate the depth to navigate up from the last saved directory to the current target
                if last_saved_directory == directory:
                    depth = 0
                else:
                    relative_path = os.path.relpath(directory, start=last_saved_directory)
                    depth = len(relative_path.split(os.sep))

                print(f"Depth to navigate up: {depth}")
                
                if directory_path:
                    os.makedirs(directory_path, exist_ok=True)

                time.sleep(2)

                last_saved_directory = directory_path
                
                pass
            else:
                
                pyautogui.write(line + "\n")
                pyautogui.hotkey('home')

        # Save and Name file.
        pyautogui.hotkey('ctrl', 's')
        time.sleep(1)

        navigate_up(depth)
        
        pyautogui.write(filename, interval=0.1)
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)

        # Check if index of current code block is not last in list.
        if idx1 is not (len(code_blocks) - 1):
            pyautogui.hotkey('ctrl', 'n')

send_request()
