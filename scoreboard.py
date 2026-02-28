import json
import os
import tkinter as tk
from tkinter import ttk
import glob


def load_scores(folder = 'saved_games/'):

    folder_path = 'saved_games/'
    json_files = glob.glob(os.path.join(folder_path, '*json'))
    json_data = []

    for file in json_files:
        try:
            with open(file, 'r', encoding = 'utf-8') as f:
                data = json.load(f)
                json_data.append(data)
                print(f"Read {file}")
        except FileNotFoundError:
            print(f"Error: The file {file} was not found.")
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from the file.")

    return json_data


class ScoreBoardWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Scoreboard")
        self.geometry("400x300")

        # title
        tk.Label(self, text = "SCOREBOARD", font= ("Segoe UI", 18, "bold")).grid(row=0, column=0, columnspan=3)

        tk.Label(self, text = "Player", font= ("Segoe UI", 12, "bold")).grid(row=1, column=0, padx=20)
        tk.Label(self, text = "Level", font= ("Segoe UI", 12, "bold")).grid(row=1, column=1, padx=20)
        tk.Label(self, text = "Score", font= ("Segoe UI", 12, "bold")).grid(row=1, column=2, padx=20)

        tk.Label(self, text="-" * 50, font=("Courier", 10)).grid(row=2, column=0, columnspan=3)

        scores = sorted(load_scores(), key=lambda x: x['base_score'], reverse = True)
        # displaying the player's data
        for x, score in enumerate(scores):
            tk.Label(self, text = score['player'], font= ("Segoe UI", 12)).grid(row=x+3, column=0, padx=20, pady=3)
            tk.Label(self, text = score['level'], font= ("Segoe UI", 12)).grid(row=x+3, column=1, padx=20, pady=3)
            tk.Label(self, text = score['base_score'], font= ("Segoe UI", 12)).grid(row=x+3, column=2, padx=20, pady=3)



