#!./venv/bin/python
from main import Game, Level1, Move_result, Level_up_result, Game_loader
from tkinter import messagebox, simpledialog
import tkinter as tk
import simpleaudio
import re


class Game_UI(tk.Tk):

    game: Game
    buttons: list[list[tk.Button]]

    def __init__(self, game: Game):
        super().__init__()

        self.game = game
        self.title(f"Game Level {game.level} - {game.player}")
        self.geometry(f"820x720")
        self.buttons = []

        # Frame for the game grid
        self.grid_frame = tk.Frame(self)
        self.grid_frame.grid(row=0, column=0, padx=10, pady=10)

        # Frame for the controls (score, buttons, etc.)
        self.controls_frame = tk.Frame(self)
        self.controls_frame.grid(row=1, column=0, padx=10, pady=10)

        self.draw()

    def draw(self):
        self.draw_cells()
        self.draw_controlls()

    def draw_controlls(self):
        '''Draw the controll text and buttons'''

        # Destroy existing controls if they exist
        for widget in self.controls_frame.winfo_children():
            widget.destroy()

        # score
        self.score_lable = tk.Label(self.controls_frame, text=f"Score {self.game.score}", anchor="w")
        self.score_lable.grid(row=self.game.size, column=0, columnspan=self.game.size, sticky="w", padx=10, pady=10)

        # next number to place
        self.next_move_lable = tk.Label(self.controls_frame, text=f"Now place: {self.game.cur_move}", anchor="w")
        self.next_move_lable.grid(row=self.game.size + 1, column=0, columnspan=self.game.size, sticky="w", padx=10, pady=10)

        # save and load buttons
        self.save_btn = tk.Button(self.controls_frame, text="Save Game", command=self.save_game)
        self.save_btn.grid(row=self.game.size+2, column=0, padx=10, pady=10, sticky="w")

        self.load_btn = tk.Button(self.controls_frame, text="Load Game", command=self.load_game)
        self.load_btn.grid(row=self.game.size+2, column=1, padx=10, pady=10, sticky="w")

        # clear and undo buttons
        self.clear_btn = tk.Button(self.controls_frame, text="Undo", command=self.undo)
        self.clear_btn.grid(row=self.game.size+3, column=0, padx=10, pady=10, sticky="w")

        self.undo_btn = tk.Button(self.controls_frame, text="clear", command=self.clear)
        self.undo_btn.grid(row=self.game.size+3, column=1, padx=10, pady=10, sticky="w")

    def draw_cells(self):
        '''Create all the button to display and interact the the cells'''
        # destroy any existing cells
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        self.buttons = []

        # draw grid for x, y
        for y in range(self.game.size):
            row = []
            for x in range(self.game.size):
                # draw a cell
                btn = tk.Button(self.grid_frame, text=str(self.game.cells[x][y]), 
                                width=5, height=1, 
                                command=lambda x=x, y=y: self.on_cell_click(x, y), 
                                font=("Helvetica", 20, "bold"), bg="grey")
                
                btn.grid(row=y, column=x, padx=5, pady=5)
                if self.game.cells[x][y] != 0:
                    btn.config(bg="green")
                row.append(btn)

            self.buttons.append(row)

    def update_cells(self):
        """Updates the game grid with the latest values. as well as changing text"""
        self.score_lable.config(text=f"Score {self.game.score}")
        self.next_move_lable.config(text=f"Now place: {self.game.cur_move}")

        # go through all the cell buttons
        for y in range(self.game.size):
            for x in range(self.game.size):
                # set correct number and color
                self.buttons[y][x].config(text=str(self.game.cells[x][y]))
                if self.game.cells[x][y] != 0:
                    self.buttons[y][x].config(bg="green")
                else:
                    self.buttons[y][x].config(bg="grey")

    def on_cell_click(self, x: int, y: int):
        # attempt the move
        try_place: Move_result = self.game.place(x, y, self.game.cur_move)
        if try_place.success():
            
            simpleaudio.WaveObject.from_wave_file("sound/success.wav").play()
            # update the cells display, as well as any text that might need to change
            self.update_cells()
        else:
            # play the sound and show a popup
            simpleaudio.WaveObject.from_wave_file("sound/failure.wav").play()
            self.show_error(try_place)
            
        # see if level up occurs
        try_level_up: Level_up_result = self.game.level_up()
        if try_level_up.success():
            self.game = try_level_up.game_board()
            self.draw()
        elif try_level_up.description() == "Game is already at max level":
            messagebox.showinfo("You win!", "You won the game!")

    def show_error(self, message: str):
        """Shows an error message box."""
        messagebox.showerror("Error", message)

    def ask_for_filename(self, action: str) -> str:
        """Prompts the user for a filename."""
        filename = simpledialog.askstring(f"{action} Game", f"Enter the game's name: ")
        # clean the filename
        filename = re.sub(r"[/\\?%*:|\"<>\x7F\x00-\x1F]", "-", filename)
        return filename.strip() if filename else None

    def save_game(self):
        """Saves the current game."""
        filename = self.ask_for_filename("Save")
        if not filename:
            return None
        Game_loader.save_game(self.game, filename)

    def load_game(self):
        """Loads a saved game."""
        filename = self.ask_for_filename("Load")
        if not filename:
            return None
        try:
            self.game = Game_loader.load_game(filename)
        except FileNotFoundError:
            self.show_error("File could not be found")
        self.title(f"Game Level {self.game.level} - {self.game.player}")
        self.draw()

    def undo(self):
        '''Undo the most recent move'''
        self.game.undo()
        self.update_cells()


    def clear(self):
        '''Undo every move'''
        self.game.clear()
        self.update_cells()



if __name__ == "__main__":
    player_name = simpledialog.askstring(f"new Game", f"Enter your Name: ")
    game_instance = Level1(player_name, 5)
    app = Game_UI(game_instance)
    app.mainloop()
