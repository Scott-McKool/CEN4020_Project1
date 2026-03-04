import json
import os
import tkinter as tk
import glob
from game import Level1


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



def calc_score(data):
    score = data['base_score']

    if data['level'] == 2:
        return score
    
    cells = data['cells']
    
    def find_value(val):
        for y, row in enumerate(cells):
            for x, cell in enumerate(row):
                if cell == val:
                    return(x,y)

        return None
    
    cur_p = find_value(1)

    if cur_p is None:
        return score
    
    value = 1
    while True:
        next_p = find_value(value + 1)
        if next_p is None:
            break
        x,y = cur_p
        px, py = next_p
        if abs(x-px) == abs(y-py):
            score += 1
        cur_p = next_p
        value += 1

    return score



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

        scores = load_scores()
        final_scores = sorted(scores, key=lambda x: calc_score(x), reverse = True)
        # displaying the player's data
        for x, score in enumerate(final_scores):
            actual_score = calc_score(score)
            tk.Label(self, text = score['player'], font= ("Segoe UI", 12)).grid(row=x+3, column=0, padx=20, pady=3)
            tk.Label(self, text = score['level'], font= ("Segoe UI", 12)).grid(row=x+3, column=1, padx=20, pady=3)
            tk.Label(self, text = actual_score, font= ("Segoe UI", 12)).grid(row=x+3, column=2, padx=20, pady=3)



