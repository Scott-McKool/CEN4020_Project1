from sys import exit
import tkinter as tk
from tkinter import ttk
from playsound import playsound
from main import *

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
        self.lvl1inputframe.columnconfigure(0, weight=1)
        self.lvl1inputframe.columnconfigure(1, weight=1)

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
        self.entryButton.grid(column=0, row=3, sticky='w', padx=5, pady=5)

        self.currentNum = tk.Label(self.lvl1inputframe, text=f"Next number: {self.gameobj.cur_move}")
        self.currentNum.grid(column=1, row=3, sticky='ew', padx=5, pady=5)

        self.gamegridGUI()

        self.root.mainloop()

    def gamegridInit(self):
        self.lvl1gridframe.grid = []
        for i in range(5):
            row = []
            for j in range(5):
                cell = tk.Label(self.lvl1gridframe, text=f" ", bg="white", borderwidth=1, relief="solid", font=("Helvetica", 10), width = 8, height=4, padx=5, pady=5)
                cell.grid(row=i, column=j, sticky='nsew')
                row.append(cell)
            self.lvl1gridframe.grid.append(row)
            self.lvl1grid.append(row)

    def gamegridGUI(self):
        
        for i in range(self.gameobj.size):
            for j in range(self.gameobj.size):
                if self.gameobj.cells[i][j] != 0:
                    self.lvl1grid[i][j].configure(text=f"{self.gameobj.cells[i][j]}", bg="lime")
                    
        self.currentNum.configure(text=f"Next Number: {self.gameobj.cur_move}")

    def valReturn(self):
        xret = int(self.rowEntry.get()) - 1
        yret = int(self.columnEntry.get()) - 1
        vret = int(self.valEntry.get())

        return xret, yret, vret
    
    def GUIplace(self):

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
            self.gameobj.cur_move += 1
        elif not placeRes.success():
            playsound.playsound("wrong.mp3")
            errorwindow = tk.Tk()
            errormessage = tk.Label(errorwindow, text="Error: invalid placement", padx=5, pady=5)
            errormessage.pack()
            errorwindow.mainloop()

        lvlupRes: Level_up_result = self.gameobj.level_up()

        if lvlupRes.success():
            self.gamegridGUI()
            playsound.playsound("correct.mp3")
            winwindow = tk.Tk()
            winmessage = tk.Label(winwindow, text="You Win!", padx=5, pady=5)
            winmessage.pack()
            winwindow.mainloop()
            return

        self.gamegridGUI()

    def __del__(self):
        self.root.quit()

if __name__ == "__main__":
    newGame: Game = Level1(5)
    newGame = Game_loader.load_game("late_game")

    gameGUI: lvl1gameWindow = lvl1gameWindow(newGame)

    while True:

        # print(newGame)
        # in_str: str = input("enter your move 'x y value' (s=save, l=load, q=quit):")

        # if in_str == "q":
        #     exit()

        # if in_str == "s":
        #     in_str = input("Choose a filename for your game: ")
        #     Game_loader.save_game(newGame, in_str)
        #     continue

        # if in_str == "l":
        #     in_str = input("type the game file to load: ")
        #     newGame = Game_loader.load_game(in_str)
        #     continue

        # x, y, value = lvl1gameWindow.valReturn()
        # place_result: Move_result = newGame.place(x, y, value)

        # if place_result.success():
        #     playsound.playsound("correct.mp3", block=False)
        # elif not place_result.success():
        #     playsound.playsound("wrong.mp3", block=False)
        #     errorwindow = tk.Tk()
        #     errormessage = tk.Label(errorwindow, text="Error: invalid placement", padx=5, pady=5)
        #     errormessage.pack()
        #     errorwindow.mainloop()
        
        

        gameGUI.gamegridGUI()