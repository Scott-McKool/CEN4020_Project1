import tkinter as tk
from tkinter import ttk
from main import *

root = tk.Tk()
root.title("Grid test")
# root.state("zoomed")

lvl1gridframe = tk.Frame(root, padx = 10, pady=10, borderwidth=1, relief="solid")
lvl1gridframe.pack(anchor="nw")

count = 0

lvl1grid = []

def fillNum(grid, rowval: int, colval: int):
    global count

    if grid[rowval][colval]['text'] == " ":
        grid[rowval][colval].configure(text=f"{count+1}")
        count += 1
    else:
        errorwindow = tk.Tk()
        errorwindow.title("Error")
        errormessage = tk.Label(errorwindow, text="Sorry! That is an invalid square, please try again.", padx=10, pady=10)
        errormessage.pack()

def gamegrid(fivegrid):
    global lvl1grid

    fivegrid.grid = []
    for i in range(5):
        row = []
        for j in range(5):
            cell = tk.Label(fivegrid, text=f" ", bg="white", borderwidth=1, relief="solid", font=("Helvetica", 10), width = 8, height=4, padx=5, pady=5)
            cell.grid(row=i, column=j, sticky='nsew')
            row.append(cell)
        fivegrid.grid.append(row)
        lvl1grid.append(row)

gamegrid(lvl1gridframe)

lvl1inputframe = tk.Frame(root, padx=10, pady=10)
lvl1inputframe.pack(anchor="sw")

lvl1inputframe.rowconfigure(0, weight=1)
lvl1inputframe.rowconfigure(1, weight=1)
lvl1inputframe.rowconfigure(2, weight=1)
lvl1inputframe.columnconfigure(0, weight=1)
lvl1inputframe.columnconfigure(1, weight=1)

rowLabel = tk.Label(lvl1inputframe, text="Enter row: ")
rowLabel.grid(column=0, row=0, sticky='e', padx=5, pady=5)

rowEntry = tk.Entry(lvl1inputframe)
rowEntry.grid(column=1, row=0, sticky='ew', padx=5, pady=5)

columnLabel = tk.Label(lvl1inputframe, text="Enter column: ")
columnLabel.grid(column=0, row=1, sticky='ew', padx=5, pady=5)

columnEntry = tk.Entry(lvl1inputframe)
columnEntry.grid(column=1, row=1, sticky='ew', padx=5, pady=5)

entryButton = tk.Button(lvl1inputframe, text="Place Number", command=lambda: fillNum(lvl1grid, int(rowEntry.get()), int(columnEntry.get())))
entryButton.grid(column=0, row=2, sticky='w', padx=5, pady=5)

root.mainloop()