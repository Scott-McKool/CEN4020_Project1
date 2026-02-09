from sys import exit
import tkinter as tk
from tkinter import ttk
from playsound import playsound
from main import *

lvl2game: Game

class lvl1gameWindow():
    gameobj: Game
    root: tk.Tk
    lvl1gridframe: tk.Frame
    lvl1inputframe: tk.Frame
    lvl1grid: list
    rowLabel : tk.Label
    columnLabel: tk.Label
    valLabel: tk.Label
    rowEntry: tk.Entry
    columnEntry: tk.Entry
    valEntry: tk.Entry
    entryButton: tk.Button
    currentNum: tk.Label
    saveButton: tk.Button
    loadButton: tk.Button
    undoButton: tk.Button
    clearButton: tk.Button
    currentScore: tk.Label
    playersetButton: tk.Button
    playersetEntry: tk.Entry

    def __init__(self, game: Game):
        self.gameobj = game
        self.root = tk.Tk()
        self.root.title("Level 1")
        self.lvl1gridframe = tk.Frame(self.root, padx = 10, pady=10, borderwidth=1, relief="solid")
        self.lvl1gridframe.pack(anchor="nw")

        self.lvl1grid = []
        self.gamegridInit()

        self.lvl1inputframe = tk.Frame(self.root, padx=10, pady=10)
        self.lvl1inputframe.pack(anchor="sw")

        self.lvl1inputframe.rowconfigure(0, weight=1)
        self.lvl1inputframe.rowconfigure(1, weight=1)
        self.lvl1inputframe.rowconfigure(2, weight=1)
        self.lvl1inputframe.rowconfigure(3, weight=1)
        self.lvl1inputframe.rowconfigure(4, weight=1)
        self.lvl1inputframe.rowconfigure(5, weight=1)
        self.lvl1inputframe.columnconfigure(0, weight=1)
        self.lvl1inputframe.columnconfigure(1, weight=1)
        self.lvl1inputframe.columnconfigure(2, weight=1)

        self.rowLabel = tk.Label(self.lvl1inputframe, text="Enter row: ")
        self.rowLabel.grid(column=0, row=0, sticky='e', padx=5, pady=5)

        self.rowEntry = tk.Entry(self.lvl1inputframe)
        self.rowEntry.grid(column=1, row=0, sticky='ew', padx=5, pady=5)

        self.columnLabel = tk.Label(self.lvl1inputframe, text="Enter column: ")
        self.columnLabel.grid(column=0, row=1, sticky='ew', padx=5, pady=5)

        self.columnEntry = tk.Entry(self.lvl1inputframe)
        self.columnEntry.grid(column=1, row=1, sticky='ew', padx=5, pady=5)

        self.valLabel = tk.Label(self.lvl1inputframe, text="Enter Value: ")
        self.valLabel.grid(column=0, row=2, sticky='ew', padx=5, pady=5)

        self.valEntry = tk.Entry(self.lvl1inputframe)
        self.valEntry.grid(column=1, row=2, sticky='ew', padx=5, pady=5)

        self.entryButton = tk.Button(self.lvl1inputframe, text="Place Number", command=lambda: self.GUIplace())
        self.entryButton.grid(column=2, row=4, sticky='w', padx=5, pady=5)

        self.currentNum = tk.Label(self.lvl1inputframe, text=f"Next number: {self.gameobj.cur_move}")
        self.currentNum.grid(column=1, row=3, sticky='ew', padx=5, pady=5)

        self.currentScore = tk.Label(self.lvl1inputframe, text=f"Current score: {self.gameobj.score}")
        self.currentScore.grid(column=0, row=3, sticky='ew', padx=5, pady=5)

        self.playersetButton = tk.Button(self.lvl1inputframe, text="Type player name:", command=lambda: self.setPlayer())
        self.playersetButton.grid(column=0, row=5, sticky='ew', padx=5, pady=5)

        self.playersetEntry = tk.Entry(self.lvl1inputframe)
        self.playersetEntry.grid(column=1, row=5, sticky='ew', padx=5, pady=5)

        self.saveButton = tk.Button(self.lvl1inputframe, text="Save Game", command=lambda: self.saveGUI())
        self.saveButton.grid(column=2, row=0, sticky='ew', padx=5, pady=5)

        self.loadButton = tk.Button(self.lvl1inputframe, text="Load Game", command=lambda: self.LoadGUI())
        self.loadButton.grid(column=2, row=1, sticky='ew', padx=5, pady=5)

        self.undoButton = tk.Button(self.lvl1inputframe, text="Undo Move", command=lambda: self.undoGUI())
        self.undoButton.grid(column=2, row=2, sticky='ew', padx=5, pady=5)

        self.clearButton = tk.Button(self.lvl1inputframe, text="Clear Board", command=lambda: self.clearGUI())
        self.clearButton.grid(column=2, row=3, sticky='ew', padx=5, pady=5)

        self.gamegridGUI()

        self.root.mainloop()

    def gamegridInit(self):
        self.lvl1gridframe.grid = []
        self.lvl1grid = []
        for i in range(self.gameobj.size):
            row = []
            for j in range(self.gameobj.size):
                cell = tk.Label(self.lvl1gridframe, text=f" ", bg="white", borderwidth=1, relief="solid", font=("Helvetica", 10), width = 8, height=4, padx=5, pady=5)
                cell.grid(row=i, column=j, sticky='nsew')
                row.append(cell)
            self.lvl1gridframe.grid.append(row)
            self.lvl1grid.append(row)

    def gamegridGUI(self, color: str = "lime"):
        
        for i in range(self.gameobj.size):
            for j in range(self.gameobj.size):
                if self.gameobj.cells[i][j] != 0:
                    self.lvl1grid[i][j].configure(text=f"{self.gameobj.cells[i][j]}", bg=color)
                    
        self.currentNum.configure(text=f"Next Number: {self.gameobj.cur_move}")
        self.currentScore.configure(text=f"Current Score: {self.gameobj.score}")

    def valReturn(self):
        xret = int(self.rowEntry.get()) - 1
        yret = int(self.columnEntry.get()) - 1
        vret = int(self.valEntry.get())

        return xret, yret, vret
    
    def GUIplace(self):
        global lvl2game

        x, y, value = self.valReturn()
        if value != self.gameobj.cur_move:
            playsound.playsound("wrong.mp3")
            errorwindow = tk.Tk()
            errormessage = tk.Label(errorwindow, text="Error: invalid value", padx=5, pady=5)
            errormessage.pack()
            errorwindow.mainloop()
            return
        
        placeRes: Move_result = self.gameobj.place(x, y, value)

        if placeRes.success():
            playsound.playsound("correct.mp3")

        elif not placeRes.success():
            playsound.playsound("wrong.mp3")
            errorwindow = tk.Tk()
            errormessage = tk.Label(errorwindow, text=f"Error: {placeRes.description()}", padx=5, pady=5)
            errormessage.pack()
            errorwindow.mainloop()

        lvlupRes: Level_up_result = self.gameobj.level_up()

        if lvlupRes.success():
            self.gamegridGUI()
            playsound.playsound("correct.mp3")
            winwindow = tk.Tk()
            winmessage = tk.Label(winwindow, text="You win level 1! Now onto Level 2...", padx=5, pady=5)
            winmessage.pack()
            winwindow.mainloop()

            self.gameobj = lvlupRes.game_board()
            lvl2gameGUI: lvl2gameWindow = lvl2gameWindow(self.gameobj)
            return

        self.gamegridGUI()

    def setPlayer(self):
        self.gameobj.player = self.playersetEntry.get()

    def saveGUI(self):
        saveWindow = tk.Tk()
        saveWindow.rowconfigure(0, weight=1)
        saveWindow.rowconfigure(1, weight=2)
        saveWindow.columnconfigure(0, weight=1)
        saveWindow.columnconfigure(1, weight=1)

        saveLabel = tk.Label(saveWindow, text="Enter file name (without extension):", padx=5, pady=5)
        saveLabel.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

        saveEntry = tk.Entry(saveWindow)
        saveEntry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)

        saveBut = tk.Button(saveWindow, text="Save", padx=5, pady=5, command=lambda: Game_loader.save_game(self.gameobj, saveEntry.get()))
        saveBut.grid(row=1, column=0, sticky='ew', padx=5, pady=5)

        saveWindow.mainloop()

    def LoadGUI(self):
        loadWindow = tk.Tk()
        loadWindow.rowconfigure(0, weight=1)
        loadWindow.rowconfigure(1, weight=2)
        loadWindow.columnconfigure(0, weight=1)
        loadWindow.columnconfigure(1, weight=1)

        loadLabel = tk.Label(loadWindow, text="Enter file name (without extension):", padx=5, pady=5)
        loadLabel.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

        loadEntry = tk.Entry(loadWindow)
        loadEntry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)

        loadBut = tk.Button(loadWindow, text="Load", padx=5, pady=5, command=lambda: self.helperloadGUI(loadEntry.get()))
        loadBut.grid(row=1, column=0, sticky='ew', padx=5, pady=5)

        loadWindow.mainloop()

    def helperloadGUI(self, loadEntry: str):
        self.gameobj = Game_loader.load_game(loadEntry)
        if self.gameobj.level == 2:
            lvl2gameGUI: lvl2gameWindow = lvl2gameWindow(self.gameobj)
        else:
            self.gamegridInit()
            self.gamegridGUI()

    def undoGUI(self):
        undoobj = self.gameobj.undo()
        if undoobj.success() != True:
            errorwindow = tk.Tk()
            errormessage = tk.Label(errorwindow, text=f"Cannot undo.", padx=5, pady=5)
            errormessage.pack()
            errorwindow.mainloop()

        self.gamegridInit()
        self.gamegridGUI()

    def clearGUI(self):
        self.gameobj.clear()
        self.gamegridInit()
        self.gamegridGUI()

    def __del__(self):
        self.root.quit()

class lvl2gameWindow():
    gameobj: Game
    root: tk.Tk
    lvl1gridframe: tk.Frame
    lvl1inputframe: tk.Frame
    lvl1grid: list
    rowLabel : tk.Label
    columnLabel: tk.Label
    valLabel: tk.Label
    rowEntry: tk.Entry
    columnEntry: tk.Entry
    valEntry: tk.Entry
    entryButton: tk.Button
    currentNum: tk.Label
    saveButton: tk.Button
    loadButton: tk.Button
    undoButton: tk.Button
    clearButton: tk.Button
    currentScore: tk.Label
    playersetButton: tk.Button
    playersetEntry: tk.Entry

    def __init__(self, game: Game):
        self.gameobj = game
        self.root = tk.Tk()
        self.root.title("Level 2")
        self.lvl1gridframe = tk.Frame(self.root, padx = 10, pady=10, borderwidth=1, relief="solid")
        self.lvl1gridframe.pack(anchor="nw")

        self.lvl1grid = []
        self.gamegridInit()

        self.lvl1inputframe = tk.Frame(self.root, padx=10, pady=10)
        self.lvl1inputframe.pack(anchor="sw")

        self.lvl1inputframe.rowconfigure(0, weight=1)
        self.lvl1inputframe.rowconfigure(1, weight=1)
        self.lvl1inputframe.rowconfigure(2, weight=1)
        self.lvl1inputframe.rowconfigure(3, weight=1)
        self.lvl1inputframe.rowconfigure(4, weight=1)
        self.lvl1inputframe.columnconfigure(0, weight=1)
        self.lvl1inputframe.columnconfigure(1, weight=1)
        self.lvl1inputframe.columnconfigure(2, weight=1)

        self.rowLabel = tk.Label(self.lvl1inputframe, text="Enter row: ")
        self.rowLabel.grid(column=0, row=0, sticky='e', padx=5, pady=5)

        self.rowEntry = tk.Entry(self.lvl1inputframe)
        self.rowEntry.grid(column=1, row=0, sticky='ew', padx=5, pady=5)

        self.columnLabel = tk.Label(self.lvl1inputframe, text="Enter column: ")
        self.columnLabel.grid(column=0, row=1, sticky='ew', padx=5, pady=5)

        self.columnEntry = tk.Entry(self.lvl1inputframe)
        self.columnEntry.grid(column=1, row=1, sticky='ew', padx=5, pady=5)

        self.valLabel = tk.Label(self.lvl1inputframe, text="Enter Value: ")
        self.valLabel.grid(column=0, row=2, sticky='ew', padx=5, pady=5)

        self.valEntry = tk.Entry(self.lvl1inputframe)
        self.valEntry.grid(column=1, row=2, sticky='ew', padx=5, pady=5)

        self.entryButton = tk.Button(self.lvl1inputframe, text="Place Number", command=lambda: self.GUIplace())
        self.entryButton.grid(column=2, row=4, sticky='w', padx=5, pady=5)

        self.currentNum = tk.Label(self.lvl1inputframe, text=f"Next number: {self.gameobj.cur_move}")
        self.currentNum.grid(column=1, row=3, sticky='ew', padx=5, pady=5)

        self.currentScore = tk.Label(self.lvl1inputframe, text=f"Current score: {self.gameobj.score}")
        self.currentScore.grid(column=0, row=3, sticky='ew', padx=5, pady=5)

        self.playersetButton = tk.Button(self.lvl1inputframe, text="Type player name:", command=lambda: self.setPlayer())
        self.playersetButton.grid(column=0, row=3, sticky='ew', padx=5, pady=5)

        self.playersetEntry = tk.Entry(self.lvl1inputframe)
        self.playersetEntry.grid(column=1, row=3, sticky='ew', padx=5, pady=5)

        self.saveButton = tk.Button(self.lvl1inputframe, text="Save Game", command=lambda: self.saveGUI())
        self.saveButton.grid(column=2, row=0, sticky='ew', padx=5, pady=5)

        self.loadButton = tk.Button(self.lvl1inputframe, text="Load Game", command=lambda: self.LoadGUI())
        self.loadButton.grid(column=2, row=1, sticky='ew', padx=5, pady=5)

        self.undoButton = tk.Button(self.lvl1inputframe, text="Undo Move", command=lambda: self.undoGUI())
        self.undoButton.grid(column=2, row=2, sticky='ew', padx=5, pady=5)

        self.clearButton = tk.Button(self.lvl1inputframe, text="Clear Board", command=lambda: self.clearGUI())
        self.clearButton.grid(column=2, row=3, sticky='ew', padx=5, pady=5)

        self.gamegridGUI()

        self.root.mainloop()

    def gamegridInit(self):
        self.lvl1gridframe.grid = []
        self.lvl1grid = []
        for i in range(7):
            row = []
            for j in range(7):
                cell = tk.Label(self.lvl1gridframe, text=f" ", bg="white", borderwidth=1, relief="solid", font=("Helvetica", 10), width = 8, height=4, padx=5, pady=5)
                cell.grid(row=i, column=j, sticky='nsew')
                row.append(cell)
            self.lvl1gridframe.grid.append(row)
            self.lvl1grid.append(row)

    def gamegridGUI(self):
        
        for i in range(self.gameobj.size):
            for j in range(self.gameobj.size):
                if self.gameobj.cells[i][j] != 0:
                    if (i == 0 or i == 6) and (j == 0 or j == 6):
                        self.lvl1grid[i][j].configure(text=f"{self.gameobj.cells[i][j]}", bg="yellow")
                    elif (i == 0 or i == 6) or (j == 0 or j == 6):
                        self.lvl1grid[i][j].configure(text=f"{self.gameobj.cells[i][j]}", bg="cyan")
                    else:
                        self.lvl1grid[i][j].configure(text=f"{self.gameobj.cells[i][j]}", bg="lime")
                    
        self.currentNum.configure(text=f"Next Number: {self.gameobj.cur_move}")
        self.currentScore.configure(text=f"Current Score: {self.gameobj.score}")

    def valReturn(self):
        xret = int(self.rowEntry.get()) - 1
        yret = int(self.columnEntry.get()) - 1
        vret = int(self.valEntry.get())

        return xret, yret, vret
    
    def GUIplace(self):

        x, y, value = self.valReturn()
        
        placeRes: Move_result = self.gameobj.place(x, y, value)

        if placeRes.success():
            self.gamegridGUI()
            playsound.playsound("correct.mp3")
        elif not placeRes.success():
            playsound.playsound("wrong.mp3")
            errorwindow = tk.Tk()
            errormessage = tk.Label(errorwindow, text=f"Error: {placeRes.description()}", padx=5, pady=5)
            if placeRes.description() == "Space is already filled.":
                self.undoGUI
            errormessage.pack()
            errorwindow.mainloop()

        if self.winChecker() == True:
            playsound.playsound("correct.mp3")
            winwindow = tk.Tk()
            winmessage = tk.Label(winwindow, text="You win level 2, and the game!", padx=5, pady=5)
            winmessage.pack()
            self.saveGUI()
            winwindow.mainloop()
            

        self.gamegridGUI()

    def winChecker(self) -> bool:
        winChecker = True

        for i in range(self.gameobj.size):
            for j in range(self.gameobj.size):
                if self.gameobj.cells[i][j] == 0:
                    winChecker = False
        
        return winChecker

    def setPlayer(self):
        self.gameobj.player = self.playersetEntry.get()

    def saveGUI(self):
        saveWindow = tk.Tk()
        saveWindow.rowconfigure(0, weight=1)
        saveWindow.rowconfigure(1, weight=2)
        saveWindow.columnconfigure(0, weight=1)
        saveWindow.columnconfigure(1, weight=1)

        saveLabel = tk.Label(saveWindow, text="Enter file name (without extension):", padx=5, pady=5)
        saveLabel.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

        saveEntry = tk.Entry(saveWindow)
        saveEntry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)

        saveBut = tk.Button(saveWindow, text="Save", padx=5, pady=5, command=lambda: Game_loader.save_game(self.gameobj, saveEntry.get()))
        saveBut.grid(row=1, column=0, sticky='ew', padx=5, pady=5)

        saveWindow.mainloop()

    def LoadGUI(self):
        loadWindow = tk.Tk()
        loadWindow.rowconfigure(0, weight=1)
        loadWindow.rowconfigure(1, weight=2)
        loadWindow.columnconfigure(0, weight=1)
        loadWindow.columnconfigure(1, weight=1)

        loadLabel = tk.Label(loadWindow, text="Enter file name (without extension):", padx=5, pady=5)
        loadLabel.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

        loadEntry = tk.Entry(loadWindow)
        loadEntry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)

        loadBut = tk.Button(loadWindow, text="Load", padx=5, pady=5, command=lambda: self.helperloadGUI(loadEntry.get()))
        loadBut.grid(row=1, column=0, sticky='ew', padx=5, pady=5)

        loadWindow.mainloop()

    def helperloadGUI(self, loadEntry: str):
        self.gameobj = Game_loader.load_game(loadEntry)
        self.gamegridInit()
        self.gamegridGUI()

    def undoGUI(self):
        undoobj = self.gameobj.undo()
        if undoobj.success() != True:
            errorwindow = tk.Tk()
            errormessage = tk.Label(errorwindow, text=f"Cannot undo.", padx=5, pady=5)
            errormessage.pack()
            errorwindow.mainloop()

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

    lvl1gameGUI: lvl1gameWindow = lvl1gameWindow(newGame)

    exit(0)