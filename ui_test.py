import tkinter as tk
from tkinter import ttk
from main import *

root = tk.Tk()
root.title("Grid test")

gridframe = tk.Frame(root, padx = 10, pady=10)
gridframe.pack()

def gamegrid(fivegrid):
    count = 0
    fivegrid.grid = []
    for i in range(5):
        row = []
        for j in range(5):
            row.append(tk.Label(fivegrid, text=f"{count+1}", bg="white", ).grid(row=i, column=j, sticky='nsew'))
            count += 1
        fivegrid.grid.append(row)

gamegrid(gridframe)

root.mainloop()