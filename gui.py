#!./venv/bin/python3
from main import Game, Result, Game_loader, Level1
import string
from tkinter import simpledialog
from tkinter import messagebox
import simpleaudio as sa
from tkinter import ttk
import tkinter as tk
from sys import exit

class gameWindow():
    gameobj: Game
    root: tk.Tk
    gridframe: tk.Frame
    inputframe: tk.Frame
    grid: list
    entryButton: tk.Button
    currentNum: tk.Label
    saveButton: tk.Button
    loadButton: tk.Button
    undoButton: tk.Button
    clearButton: tk.Button
    levelupButton: tk.Button
    themebutton: tk.Button
    currentScore: tk.Label
    playersetButton: tk.Button
    playersetEntry: tk.Entry
    yay: sa.WaveObject
    unyay: sa.WaveObject
    themes: dict
    themeselect: string

    def __init__(self, game: Game):
        self.gameobj = game
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
        self.inputframe.columnconfigure(0, weight=1)
        self.inputframe.columnconfigure(1, weight=1)
        self.inputframe.columnconfigure(2, weight=1)

        self.currentNum = tk.Label(self.inputframe, text=f"Next number: {self.gameobj.cur_move}", fg=self.themes[self.themeselect][4], bg=self.themes[self.themeselect][0])
        self.currentNum.grid(column=1, row=0, sticky='ew', padx=5, pady=5)

        self.currentScore = tk.Label(self.inputframe, text=f"Current score: {self.gameobj.score()}", fg=self.themes[self.themeselect][4], bg=self.themes[self.themeselect][0])
        self.currentScore.grid(column=0, row=0, sticky='ew', padx=5, pady=5)

        self.playersetButton = tk.Button(self.inputframe, text="Type player name:", command=lambda: self.setPlayer(), fg=self.themes[self.themeselect][4], bg=self.themes[self.themeselect][0])
        self.playersetButton.grid(column=0, row=1, sticky='ew', padx=5, pady=5)

        self.playersetEntry = tk.Entry(self.inputframe)
        self.playersetEntry.grid(column=1, row=1, sticky='ew', padx=5, pady=5)

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

        self.themebutton = tk.Button(self.inputframe, text="Select Theme", command=lambda: self.themerefresh(), fg=self.themes[self.themeselect][4], bg=self.themes[self.themeselect][0])
        self.themebutton.grid(column=2, row=5, sticky='ew', padx=5, pady=5)

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
                    if self.gameobj.level == 2:
                        if (i == 0 or i == 6) and (j == 0 or j == 6):
                            self.grid[i][j].configure(text=f"{self.gameobj.cells[i][j]}", bg="yellow")
                        elif (i == 0 or i == 6) or (j == 0 or j == 6):
                            self.grid[i][j].configure(text=f"{self.gameobj.cells[i][j]}", bg="cyan")
                        else:
                            self.grid[i][j].configure(text=f"{self.gameobj.cells[i][j]}", bg="lime")
                    else:
                        self.grid[i][j].configure(text=f"{self.gameobj.cells[i][j]}", bg="lime")

        if self.gameobj.level == 1:
            self.currentNum.configure(text=f"Next Number: {self.gameobj.cur_move}")
            self.currentScore.configure(text=f"Current Score: {self.gameobj.score()}")
    

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
        self.gamegridGUI()

    def placeGUI(self, x, y, value):

        if self.gameobj.level == 1:
            if value != self.gameobj.cur_move:
                messagebox.showerror(title="Value Error", message="Error: invalid value")
                return
            else:
                placeval = value
        elif self.gameobj.level == 2:
            placeval = simpledialog.askinteger(title="Enter Value", prompt="Enter value to be placed")
            if placeval == None:
                return
        
        placeRes: Result = self.gameobj.place(x, y, placeval)

        if placeRes.success():
            yay_play = self.yay.play()

        elif not placeRes.success():
            unyay_play = self.unyay.play()
            messagebox.showerror(title="Place Error", message=f"Error: {placeRes.description()}")

        if self.winChecker() == True:
            if self.gameobj.level == 1:
                self.gamegridGUI()
                messagebox.showinfo(title="Yay!", message="You win level 1! Click on the \"Level Up\" button to move to Level 2.")
            else:
                messagebox.showinfo(title="Yay^2!", message="You have won level 2, and the game! (so far...)")

        self.gamegridGUI()

    def setPlayer(self):
        self.gameobj.player = self.playersetEntry.get()

    def levelUp(self):
        lvlupRes: Result = self.gameobj.level_up()
        if lvlupRes.success():
            self.gameobj = lvlupRes.obj()
            self.gamegridInit()
            self.gamegridGUI()
            self.currentNum.configure(text=f"")
            self.currentScore.configure(text=f"")
        else:
            messagebox.showerror(title="Level Up error", message=f"Error: {lvlupRes.description()}")


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
        self.gameobj = Game_loader.load_game(loadStr).obj()
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

    def __del__(self):
        self.root.quit()

if __name__ == "__main__":
    newGame: Game = Level1("player1", 5)

    gameGUI: gameWindow = gameWindow(newGame)

    exit(0)