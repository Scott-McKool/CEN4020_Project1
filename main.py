#!./venv/bin/python3
from __future__ import annotations
from datetime import datetime
from json import load, dump
from random import randint
import playsound
import tkinter as tk

class Move_result:
    '''The result of attempting a given move, it is either successfull or not, and includes a text description of the result'''
    data: tuple[bool, str]
    def __init__(self, success: bool, description: str = "Description missing."):
        self.data = (success, description)

    def success(self) -> bool:
        '''Does the result represent a success? (true if yes, false if no)'''
        return self.data[0]
    
    def description(self) -> str:
        '''The description of the result'''
        return self.data[1] or "Description missing."
    
    def __str__(self):
        if self.success():
            return f"Successful move: {self.description()}"
        
        if not self.success():
            return f"Unsuccessfull move: {self.description()}"

class Level_up_result:
    '''the result of attampting to level up a game board, it is either a game board or None, and includes a text description'''
    data: tuple[Game | None, str]
    def __init__(self, new_game: Game | None, description: str = "Description missing."):
        self.data = (new_game, description)

    def success(self) -> bool:
        '''Did leveling up succeed?'''
        if isinstance(self.data[0], Game):
            return True
        else:
            return False

    def game_board(self) -> Game | None:
        '''The leveled up game board, or None'''
        return self.data[0]
        
    def description(self) -> str:
        '''The description of the result'''
        return self.data[1] or "Description missing."
    
    def __str__(self):
        if self.success():
            return f"Successful level up: {self.description()}"
        
        if not self.success():
            return f"Unsuccessfull level up: {self.description()}"


class Game:
    cells: list[list[int]]
    size : int
    score: int
    level: int
    log  : list[str]
    player: str
    cur_move: int
    diagflag: bool
    def __init__(self, size: int):
        self.cur_move = 2
        self.level = None
        self.size = size
        self.score = 0
        self.log = list()
        # init cell values 
        self.cells = [[0]*size for _ in range(size)]
        self.diagflag = False
        self.next_number = 2 # L1 begins 
        self.move_stack = [] # undo
        self.one_p = None # initial positions of x and y
        self.log = []
    
    def place(self, x: int, y: int, value: int = None) -> Move_result:
        '''Attempt to place a value at a given coordinate within the rules of the game. x and y are index values'''
        # make sure coords are in-bounds
        if x >= self.size or y >= self.size or x < 0 or y < 0:
            return Move_result(False, "Given coordinates are out of bounds.")
        
        # make sure space in unnoccupied
        if self.cells[x][y] != 0:
            return Move_result(False, "Space is already filled.")
        
        move_hist = { "x": x, "y": y, "prev_cell" : self.cells[x][y], 
                     "prev_score": self.score, "next": self.cur_move
        }
        
        self.move_stack.append(move_hist)
        placed = self.cur_move
        self.cells[x][y] = placed
        if placed == 1:
            self.last_move = (x,y)

        # self.cur_move += 1

        # ok to proceed
        return Move_result(True, f"Value placed {placed}")
        

    def level_up(self) -> Level_up_result:
        '''Attempt to premote the game board to the next level'''
        # make sure all cells are filled
        for row in self.cells:
            for cell in row:
                if cell == 0:
                    return Level_up_result(None, "All spaces must be filled before moving to the next level")

        # is premotion possible?
        if Game_loader.levels[self.level + 1]:
            # make a new game object based on this game, at the next higher level
            cls = Game_loader.levels[self.level + 1]
            # make new instance of the required type
            # the type will alsways be lvl2 or more, and take a lower level game as its argument
            new_game: Game = cls(self)
            new_game.add_log("level up", f"leveled up from level {self.level} to level {new_game.level}")
            return Level_up_result(new_game, f"Premoted from level {self.level} to level {new_game.level}") 
        else:
            return Level_up_result(None, "Game is already at max level")


    def from_data(self, data: dict) -> None:
        '''Populate the object's atributes from a dictionary'''
        self.cells = data["cells"]
        self.size  = data["size"]
        self.score = data["score"]
        self.level = data["level"]
        self.player= data["player"]
        self.log   = data["log"]
        self.cur_move  = data["cur_move"]

    def __str__(self):
        result: str = ""
        # add header
        result += " +" + "---"*self.size + "+\n"

        for y in range(self.size - 1, -1, -1):
            result += str(y + 1) + "|"
            for x in range(0, self.size):
                result += str(self.cells[x][y]).rjust(3)
            result += "|\n"

        # add footer
        result += " +" + "---"*self.size + "+\n"
        result += "  "
        for i in range(self.size):
            result += str(i + 1).rjust(3)

        # add score
        result += f"\n\nScore: {self.score}"
        
        return result
    
    def get(self, x: int, y:int) -> int:
        return self.cells[x][y] # retrieve (x,y) numbers
    
    def set(self, x:int, y:int, value: int):
        self.cells[x][y] = value # set numbers at cell (x,y)
    
    # undo move
    def undo(self):
        if not self.move_stack:
            return Move_result(False, "Cannot undo.")
        
        prev = self.move_stack.pop()
        self.set(prev["x"], prev["y"], prev["prev_cell"])
        self.score = prev["prev_score"]
        self.cur_move = prev["next"]

        return Move_result(True, f"Undo successful. Next value is {self.cur_move}")
    
    
    def add_log(self, category: str, description):
        self.log.append(f"Category: {category} {description}\n")


    def clear(self) -> Move_result:
        ''' Clearing the board, but 1 stays in its main position. 1 does not get cleared'''

        # L1 board clearing
        if self.level == 1:
            try: 
                if self.last_move is None:
                    return Move_result(False, "Unable to clear, value 1 position not found.")
            except AttributeError:
                return Move_result(False, "Unable to clear, value 1 position not found.")
        
            # clearing thr grid
            for i in range(self.size):
                for t in range(self.size):
                    self.set(i, t, 0)

        # setting original position of number '1'
            first_x, first_y = self.one_p
            self.set(first_x, first_y, 1)

            # reset
            self.cur_move = 2
            self.score = 0
            self.move_stack.clear()

            return Move_result(True, "Board is now clear for Level 1.")

        # L2 board clearing
        if self.level == 2:
            # clearing edge cells on the 7x7
            for i in range(self.size):
                for t in range(self.size):
                    border = (i == 0 or i == self.size - 1 or t == 0 or t == self.size - 1)
                    if border:
                        self.set(i, t, 0)
                        
            # start value at level 2
            self.cur_move = 2
            self.move_stack.clear()
            return Move_result(True, "Outer grid cleared. ")
        
        # 
        return Move_result(False, f"Uknown Level --> {self.level} not available")


class Level1(Game):
    def __init__(self, player_name: str, size: int):
        super().__init__(size)
        self.move_stack = []
        self.level: int = 1
        self.player = player_name
        self.add_log("", f"Starting new Game:")
        self.add_log("", f"Player name: {player_name}")
        self.add_log("", f"Game started: {datetime.now()}")
        self.add_log("", f"Level 1")
        self.add_log("", f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        ### initialize board for play
        # choose location for '1'
        rand_x: int = randint(0, self.size - 1)
        rand_y: int = randint(0, self.size - 1)
        self.cells[rand_x][rand_y] = 1
        self.last_move = (rand_x, rand_y)
        self.one_p = (rand_x, rand_y)


    def place(self, x: int, y: int, value: int = None) -> Move_result:
        # does the placement pass the basic checks?
        basic_checks = super().place(x, y, value)
        if not basic_checks.success():
            return basic_checks

        # make sure space is the neighbor of its predecessor
        dx = abs(self.last_move[0] - x)
        dy = abs(self.last_move[1] - y)

        if dx > 1 or dy > 1:
            return Move_result(False, "Move must be a neighbor of its predececcor.")
        
        # asses score for the move (is move place on a diagonal)
        if dx == dy:
            self.score += 1

        # make sure value is correct (ascending order)
        if not value:
            value = self.cur_move
            self.cur_move += 1
        elif value != self.cur_move:
            return Move_result(False, f"Move's value must be 1 greater than its predecesor. {value} != {self.cur_move}")

        # make the move
        self.cells[x][y] = value
        self.last_move = (x, y)
        self.cur_move += 1
        self.add_log("move", f"Placed {value} in space ({x},{y}).")
        return Move_result(True)

    def from_data(self, data) -> None:
        self.last_move = data["last_move"]
        super().from_data(data)


class Level2(Game):
    def __init__(self, base_game: Level1):
        # a level2 board is initialized from a level1 board, but with the outer ring of spaces
        size = base_game.size + 2
        super().__init__(size)
        # inherit values from the level1 board
        self.score = base_game.score
        self.level = 2
        self.log = base_game.log
        # carry over the values from the level 1 board
        for y in range(0, base_game.size):
            for x in range(0, base_game.size):
                self.cells[x+1][y+1] = base_game.cells[x][y]
        # keep track of played numbers
        self.played = [False] * (2 * (self.size + self.size)) # array of size = perimeter of board


    def _search_in_line(self, x: int, y: int, dx: int, dy: int, value: int) -> bool:
        '''Searches in a straight line, starting from cell (x,y), and moving according to (dx, dy), searching for value returns true if found, returns false if not.
        \nx and y are index values'''
        i: int = x
        j: int = y
        # while the search is in bounds
        while i >= 0 and j >= 0 and i < self.size and j < self.size:
            # found value
            if self.cells[i][j] == value:
                return True
            i += dx
            j += dy
        # could not find value
        return False


    def place(self, x: int, y: int, value: int = None) -> Move_result:
        # does the placement pass the basic checks?
        basic_checks = super().place(x, y, value)
        if not basic_checks.success():
            return basic_checks

        # make sure number has not already been played
        if self.played[value]:
            return Move_result(False, "Each number may only be placed once.")

        # do checks for if value is present in the apropriate line
        found_value: bool
        deltaX: int = 0
        deltaY: int = 0
        if x == 0:
            deltaX = 1
        if x == self.size - 1:
            deltaX = -1
        if y == 0:
            deltaY = 1
        if y == self.size - 1:
            deltaY = -1
        found_value = self._search_in_line(x, y, deltaX, deltaY, value)

        if found_value == False:
            return Move_result(False, "The number of the move and the number in the inner board must be on a straight line.")

        # make the move
        self.cells[x][y] = value
        self.played[value] = True
        self.add_log("move", f"Placed {value} in space ({x},{y}).")
        return Move_result(True)

    def from_data(self, data) -> None:
        super().from_data(data)
        self.played = data["played"]

class Game_loader():
    levels: dict = {
        1 : Level1,
        2 : Level2
    }
        
    def save_game(game: Game, name: str):
        '''Saves a provided game object to a json text file with the provided name'''
        with open(f"saved_games/{name}.json", "wt") as outfile:
            dump(game.__dict__, outfile, indent=4)
        with open(f"saved_games/{name}.log", "wt") as outfile:
            outfile.writelines(game.log)

    def load_game(name: str) -> Game:
        '''loads a game board of the appropriate type from a json file'''
        obj: Game
        with open(f"saved_games/{name}.json") as infile:
            data = load(infile)
        
        for key, cls in Game_loader.levels.items():
            if data["level"] == key:
                # make new instance of the required type
                obj = cls.__new__(cls)
                # populate the required data
                obj.from_data(data)
                return obj


if __name__ == "__main__":
    name: str = input("please enter your name: ")
    newGame: Game = Level1(name, 5)

    while True:

        print(newGame)
        in_str: str = input("enter your move 'x y value' (s=save, l=load, q=quit):")

        if in_str == "q":
            exit()

        if in_str == "s":
            in_str = input("Choose a filename for your game: ")
            Game_loader.save_game(newGame, in_str)
            continue

        if in_str == "l":
            in_str = input("type the game file to load: ")
            newGame = Game_loader.load_game(in_str)
            continue

        x, y, val = in_str.split(" ")
        place_result: Move_result = newGame.place(int(x)-1, int(y)-1, int(val))

        if place_result.success():
            playsound.playsound("correct.mp3", block=False)
        elif not place_result.success():
            playsound.playsound("wrong.mp3", block=False)
            print(place_result)
        
        lvl_up = newGame.level_up()
        if lvl_up.success():
            newGame = lvl_up.game_board()
        