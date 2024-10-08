# Deadlocks-Auto-Code-Writer
A fun little AI code writer that takes a prompt from a user and leverages OpenAI's ChatGPT to generate code and automatically populate files in Visual Studio Code.


## How to run this code

Pull the repo down and install all dependencies using,
```
pip install -r requirements.txt
```
Once all dependencies are installed, create a .env file with this variable,
```
OPENAI_API_KEY={Your personal OpenAI Api Key}
```

You can write your request for code in the
provided request.txt file. There is already an example request in there.

Then double click the AutoCodeWriter.py to run the program.

When running the AutoCodeWriter.py file, it will ask if you want to create a workspace.
This just means creating a temporary file where all of the generated files will be saved.

## Important Notes
For proper used of this program, VSCode user settings should be changed to prevent auto closing tags and auto closing parenthesis.
If not the IDE will double up on closing tags and parenthesis potentially breaking the code being written.
