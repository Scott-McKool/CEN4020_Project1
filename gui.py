#!./venv/bin/python3
from result import Result
from game import Game, Level1, Game_loader
from solver import Solver
import string
from tkinter import simpledialog
from tkinter import messagebox
import simpleaudio as sa
import tkinter as tk
from sys import exit
import time

class gameWindow():
    gameobj: Game
    grid: list
    yay: sa.WaveObject
    unyay: sa.WaveObject
    themes: dict
    themeselect: string
    solverFlag: bool
    gameobjHolder: Game | None
    timer: int

    def __init__(self, game: Game):
        self.gameobj = game
        self.gameobjHolder = None
        self.solverFlag = False
        self.timer = 80
        self.timerScore = 0
        self.timerStart = time.time()
        self.themes = {
            "light": ["#fafafa", "#e4e5f1", "#d2d3db", "#9394a5", "#484b6a"],
            "dark": ["#181818", "#212121", "#3d3d3d", "#aaaaaa", "#ffffff"],
            "moonlit": ["#1f1951", "#5669cf", "#a186eb", "#d9aefb", "#ffaefa"],
            "mermaidheart": ["#b4a4fa", "#fbe7f5", "#f7bce3", "#baddfa", "#d8edf9"],
            "forest": ["#0f2e17", "#1f5a28", "#3c8f4c", "#78c27a", "#c9f4d0"],
            "redhot": ["#de2315", "#fe340d", "#f37714", "#e69229", "#e8b611"]
        }
        self.themeselect = "light"
        self.yay = sa.WaveObject.from_wave_file("sound/yay.wav")
        self.unyay = sa.WaveObject.from_wave_file("sound/unyay.wav")
        self.root = tk.Tk()
        self.root['bg'] = self.themes[self.themeselect][0]
        self.root.title("CEN4020 Project 1 Video Game")
        self.gridframe = tk.Frame(self.root, padx = 10, pady=10, borderwidth=1, relief="solid", bg=self.themes[self.themeselect][0])
        self.gridframe.pack(anchor="nw")

        self.grid = []
        self.gamegridInit()

        self.inputframe = tk.Frame(self.root, padx=10, pady=10, bg=self.themes[self.themeselect][0])
        self.inputframe.pack(anchor="sw")

        self.inputframe.rowconfigure(0, weight=1)
        self.inputframe.rowconfigure(1, weight=1)
        self.inputframe.rowconfigure(2, weight=1)
        self.inputframe.rowconfigure(3, weight=1)
        self.inputframe.rowconfigure(4, weight=1)
        self.inputframe.rowconfigure(5, weight=1)
        self.inputframe.rowconfigure(6, weight=1)
        self.inputframe.rowconfigure(7, weight=1)
        self.inputframe.columnconfigure(0, weight=1)
        self.inputframe.columnconfigure(1, weight=1)
        self.inputframe.columnconfigure(2, weight=1)

        self.currentNum = tk.Label(self.inputframe, text=f"Next number: {self.gameobj.cur_move}", fg=self.themes[self.themeselect][4], bg=self.themes[self.themeselect][0])
        self.currentNum.grid(column=1, row=0, sticky='ew', padx=5, pady=5)

        self.currentScore = tk.Label(self.inputframe, text=f"Current score: {int(self.gameobj.score() + self.timerScore)}", fg=self.themes[self.themeselect][4], bg=self.themes[self.themeselect][0])
        self.currentScore.grid(column=0, row=0, sticky='ew', padx=5, pady=5)

        self.playersetButton = tk.Button(self.inputframe, text="Player name:", command=lambda: self.setPlayer())
        self.playersetButton.grid(column=0, row=2, sticky='ew', padx=5, pady=5)

        self.playersetEntry = tk.Entry(self.inputframe)
        self.playersetEntry.insert(0, self.gameobj.player)
        self.playersetEntry['state'] = 'readonly'
        self.playersetEntry.grid(column=1, row=2, sticky='ew', padx=5, pady=5)

        self.timerLabel = tk.Label(self.inputframe, text=f"Time Allotted: {self.timer}", fg=self.themes[self.themeselect][4], bg=self.themes[self.themeselect][0])
        self.timerLabel.grid(column=0, row=1, sticky='ew', padx=5, pady=5)

        self.saveButton = tk.Button(self.inputframe, text="Save Game", command=lambda: self.saveGUI(), fg=self.themes[self.themeselect][4], bg=self.themes[self.themeselect][0])
        self.saveButton.grid(column=2, row=0, sticky='ew', padx=5, pady=5)

        self.loadButton = tk.Button(self.inputframe, text="Load Game", command=lambda: self.LoadGUI(), fg=self.themes[self.themeselect][4], bg=self.themes[self.themeselect][0])
        self.loadButton.grid(column=2, row=1, sticky='ew', padx=5, pady=5)

        self.undoButton = tk.Button(self.inputframe, text="Undo Move", command=lambda: self.undoGUI(), fg=self.themes[self.themeselect][4], bg=self.themes[self.themeselect][0])
        self.undoButton.grid(column=2, row=2, sticky='ew', padx=5, pady=5)

        self.clearButton = tk.Button(self.inputframe, text="Clear Board", command=lambda: self.clearGUI(), fg=self.themes[self.themeselect][4], bg=self.themes[self.themeselect][0])
        self.clearButton.grid(column=2, row=3, sticky='ew', padx=5, pady=5)

        self.levelupButton = tk.Button(self.inputframe, text="Level Up", command=lambda: self.levelUp(), fg=self.themes[self.themeselect][4], bg=self.themes[self.themeselect][0])
        self.levelupButton.grid(column=2, row=4, sticky='ew', padx=5, pady=5)

        self.scoreboardButton = tk.Button(self.inputframe, text = "Scoreboard", command = lambda: self.showScoreboard(), fg=self.themes[self.themeselect][4], bg=self.themes[self.themeselect][0])
        self.scoreboardButton.grid(column = 2, row = 5, sticky = 'ew', padx = 5, pady = 5)

        #self.themebutton = tk.Button(self.inputframe, text="Select Theme", command=lambda: self.themerefresh(), fg=self.themes[self.themeselect][4], bg=self.themes[self.themeselect][0])
        #self.themebutton.grid(column=2, row=6, sticky='ew', padx=5, pady=5)

        self.solverButton = tk.Button(self.inputframe, text="Show Solution", command=lambda: self.solverGUI(), fg=self.themes[self.themeselect][4], bg=self.themes[self.themeselect][0])
        self.solverButton.grid(column=2, row=7, sticky='ew', padx=5, pady=5)

        self.gamegridGUI()

        self.root.mainloop()

    def gamegridInit(self):
        self.gridframe.grid = []
        self.grid = []
        for i in range(self.gameobj.size):
            row = []
            for j in range(self.gameobj.size):
                cell = tk.Button(self.gridframe, text=f" ", bg=self.themes[self.themeselect][1], borderwidth=1, relief="solid", font=("Helvetica", 10), width = 8, height=4, padx=5, pady=5, command=lambda x=i, y=j: self.placeGUI(x, y, self.gameobj.cur_move))
                cell.grid(row=i, column=j, sticky='nsew')
                row.append(cell)
            self.gridframe.grid.append(row)
            self.grid.append(row)

    def gamegridGUI(self):
        
        for i in range(self.gameobj.size):
            for j in range(self.gameobj.size):
                if self.gameobj.cells[i][j] != 0:
                    if self.gameobj.level >= 2:
                        if (i == 0 or i == 6) and (j == 0 or j == 6):
                            self.grid[i][j].configure(text=f"{self.gameobj.cells[i][j]}", bg="yellow")
                        elif (i == 0 or i == 6) or (j == 0 or j == 6):
                            self.grid[i][j].configure(text=f"{self.gameobj.cells[i][j]}", bg="cyan")
                        else:
                            self.grid[i][j].configure(text=f"{self.gameobj.cells[i][j]}", bg="lime")
                    else:
                        self.grid[i][j].configure(text=f"{self.gameobj.cells[i][j]}", bg="lime")

        if self.gameobj.level == 1 or self.gameobj.level == 3: # change this to serve all levels 
            self.currentNum.configure(text=f"Next Number: {self.gameobj.cur_move}")

        self.currentScore.configure(text=f"Current Score: {self.gameobj.score() + self.timerScore}")
    

    def themerefresh(self):
        themechoice = simpledialog.askstring(title= "Theme Selector", prompt="Choose your theme: \n1: Light (default) \n2: Dark \n3: Moonlit \n4: Mermaid Heart \n5: Forest \n6: Redhot \n(type the name of the theme in the box below)")
        if themechoice == None:
            return

        if themechoice.lower() == "light":
            self.themeselect = "light"
        elif themechoice.lower() == "dark":
            self.themeselect = "dark"
        elif themechoice.lower() == "moonlit":
            self.themeselect = "moonlit"
        elif themechoice.lower() == "mermaid heart":
            self.themeselect = "mermaidheart"
        elif themechoice.lower() == "forest":
            self.themeselect = "forest"
        elif themechoice.lower() == "redhot":
            self.themeselect = "redhot"
        else:
            messagebox.showerror(title="Theme select error", message=f"Error: please select a theme from the provided list")

        self.root['bg'] = self.themes[self.themeselect][0]
        self.gridframe.configure(bg=self.themes[self.themeselect][0])
        self.gamegridInit()
        self.inputframe.configure(bg=self.themes[self.themeselect][0])
        self.currentNum.configure(fg=self.themes[self.themeselect][4], bg=self.themes[self.themeselect][0])
        self.currentScore.configure(fg=self.themes[self.themeselect][4], bg=self.themes[self.themeselect][0])
        self.playersetButton.configure(fg=self.themes[self.themeselect][4], bg=self.themes[self.themeselect][0])
        self.saveButton.configure(fg=self.themes[self.themeselect][4], bg=self.themes[self.themeselect][0])
        self.loadButton.configure(fg=self.themes[self.themeselect][4], bg=self.themes[self.themeselect][0])
        self.undoButton.configure(fg=self.themes[self.themeselect][4], bg=self.themes[self.themeselect][0])
        self.clearButton.configure(fg=self.themes[self.themeselect][4], bg=self.themes[self.themeselect][0])
        self.levelupButton.configure(fg=self.themes[self.themeselect][4], bg=self.themes[self.themeselect][0])
        self.themebutton.configure(fg=self.themes[self.themeselect][4], bg=self.themes[self.themeselect][0])
        self.scoreboardButton.configure(fg=self.themes[self.themeselect][4], bg=self.themes[self.themeselect][0])
        self.solverButton.configure(fg=self.themes[self.themeselect][4], bg=self.themes[self.themeselect][0])
        self.timerLabel.configure(fg=self.themes[self.themeselect][4], bg=self.themes[self.themeselect][0])
        self.gamegridGUI()

    def placeGUI(self, x, y, value):
        
        placeRes: Result = self.gameobj.place(x, y, value)

        if placeRes.success():
            yay_play = self.yay.play()

        elif not placeRes.success():
            unyay_play = self.unyay.play()
            messagebox.showerror(title="Place Error", message=f"Error: {placeRes.description()}")

        if self.winChecker() == True:
            if self.gameobj.level == 1:
                self.gamegridGUI()
                messagebox.showinfo(title="Yay!", message="You win level 1! Click on the \"Level Up\" button to move to Level 2.")
                self.timekeep()
                self.currentScore.configure(text=f"Current score: {int(self.gameobj.score() + self.timerScore)}")
            elif self.gameobj.level == 2:
                self.gamegridGUI()
                messagebox.showinfo(title="Yay^2!", message="You win level 2! Click on the \"Level Up\" button to move to Level 2.")
                self.timekeep()
                self.currentScore.configure(text=f"Current score: {int(self.gameobj.score() + self.timerScore)}")
            else:
                messagebox.showinfo(title="Yay^3!", message="You have won level 3, and the game! (so far...)")
                self.timekeep()
            self.currentScore.configure(text=f"Current score: {int(self.gameobj.score() + self.timerScore)}")

        self.gamegridGUI()

    def setPlayer(self):
        self.gameobj.player = self.playersetEntry.get()

    def showScoreboard(self):
        from scoreboard import ScoreBoardWindow
        ScoreBoardWindow(self.root)

    def levelUp(self):
        lvlupRes: Result = self.gameobj.level_up()
        if lvlupRes.success():
            self.gameobj = lvlupRes.obj()
            self.solverFlag = False
            self.gamegridInit()
            self.gamegridGUI()
            if self.gameobj.level == 2:
                self.currentNum.configure(text=f"") # change this to show score and current number for levels 1 and 3
                self.timer = 300
                self.timerStart = time.time()
            elif self.gameobj.level == 3:
                self.timer = 600
                self.timerStart = time.time()
            self.timerLabel.configure(text=f"Time allotted: {self.timer}")
        else:
            messagebox.showerror(title="Level Up error", message=f"Error: {lvlupRes.description()}")

    def timekeep(self):
        endTime = time.time()
        duration = endTime - self.timerStart
        self.timerScore = round(self.timer - duration)

    def winChecker(self) -> bool:
        winChecker = True

        for i in range(self.gameobj.size):
            for j in range(self.gameobj.size):
                if self.gameobj.cells[i][j] == 0:
                    winChecker = False
        
        return winChecker

    def saveGUI(self):
        saveStr = simpledialog.askstring(title="Save Game", prompt="Enter file name (without extension)", parent=self.root)
        Game_loader.save_game(self.gameobj, saveStr)

    def LoadGUI(self):
        loadStr = simpledialog.askstring(title="Load Game", prompt="Enter file name (without extension)", parent=self.root)
        loadedgame = Game_loader.load_game(loadStr)
        if loadedgame.success():
            self.gameobj = loadedgame.obj()
        else:
            messagebox.showerror(title="Load Error", message=f"Error: {loadedgame.description()}")
        self.gamegridInit()
        self.gamegridGUI()

    def undoGUI(self):
        undoobj = self.gameobj.undo()
        if undoobj.success() != True:
            messagebox.showerror(title="Undo Error", message=f"Error: {undoobj.description()}")
        self.gamegridInit()
        self.gamegridGUI()

    def clearGUI(self):
        self.gameobj.clear()
        self.gamegridInit()
        self.gamegridGUI()

    def solverGUI(self):
        if self.solverFlag == False:
            self.gameobjHolder = self.gameobj
            solvedGame = Solver.solve(self.gameobj)
            if solvedGame.success():
                self.gameobj = solvedGame.obj()
                self.solverFlag = True
                self.gamegridInit()
                self.gamegridGUI()
            else:
                messagebox.showerror(title="Solver Error", message=f"Error: {solvedGame.description()}")

        elif self.solverFlag == True:
            self.gameobj = self.gameobjHolder
            self.solverFlag = False
            self.gamegridInit()
            self.gamegridGUI()

    def __del__(self):
        self.root.quit()

if __name__ == "__main__":
    newGame: Game = Level1("player1", 5)

    gameGUI: gameWindow = gameWindow(newGame)

    exit(0)