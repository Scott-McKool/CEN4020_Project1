Source code files:

game.py - handles the backend and game logic of the project, done in python.

auth.py - handles the authorization of users and their information within the database

auth_gui.py - handles GUI window for login and registering user accounts, when compiling the executable

main.py - file used to test backend in terminal, should not be used by user.

result.py - handles the result of events within the game, such as placing and leveling up

scoreboard.py - handles the scoreboard aspect of the project according to our custom user story, includes both GUI and data fetch

solver.py - handles the process of finding a solution to the current game board

gui.py - main GUI window source code, used to run the frontend/game window

Operating System: Windows, Arch Linux (Venkata), NixOS (Scott), MacOS (Yasemin)

Languages: Python

External python modules used: simpleaudio (cexen fork), pyinstaller (check requirements.txt for external module installation)

Version control method: GitHub

IDLE: Visual Studio Code

Compilation commands:
Open terminal window in Proj1_sprint2 folder

install pyinstaller using "pip install pyinstaller"

run "pyinstaller --onefile --windowed -w 'auth_gui.py' -n 'Proj1'

Proj1.exe (or Proj1 executable in case of linux) gets created in /dist subfolder, bring Proj1.exe (or Proj1 executable) into the main Proj1 folder for it to work properly. (replace existing Proj1 executable if necessary)