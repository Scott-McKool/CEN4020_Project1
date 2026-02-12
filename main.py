#!./venv/bin/python3
from __future__ import annotations
from datetime import datetime
from json import load, dump
from random import randint

class Result:
    '''The result of attempting an action that is not guarenteed.\n
    .success() returns if the attempted action was successfull.\n
    .obj() returns either an object (if the action resuts in an object) or none.\n
    .description() returns a string that is a description of the result.'''
    data: tuple[object | None, str]
    def __init__(self, obj: object | None, description: str = "Description missing"):
        self.data = (obj, description)

    def success(self) -> bool:
        '''Did the attempted action succeed?'''
        if isinstance(self.data[0], Game):
            return True
        else:
            return False

    def obj(self) -> object | None:
        '''The returned object, or none'''
        return self.data[0]
        
    def description(self) -> str:
        '''The description of the result'''
        return self.data[1] or "Description missing."
    
    def __str__(self):
        if self.success():
            return f"Successful: {self.description()}"
        
        if not self.success():
            return f"Unsuccessful: {self.description()}"
        

class Game:
    cells: list[list[int]]
    size : int
    score: int
    level: int
    log  : list[str]
    player  : str
    cur_move: int
    history : list[tuple[int, int, int]]

    def __init__(self, size: int):
        self.cur_move = 2
        self.level = None
        self.size = size
        self.score = 0
        self.log = list()
        self.history = list()
        # init cell values 
        self.cells = [[0]*size for _ in range(size)]
        # add header to log
    
    def can_place(self, x: int, y: int, value: int) -> Result:
        '''Checks if it is valid to place a value at a given coordinate within the rules of the game. x and y are index values'''

        # make sure coords are in-bounds
        if x >= self.size or y >= self.size or x < 0 or y < 0:
            return Result(False, "Given coordinates are out of bounds.")
        
        # make sure space in unnoccupied
        if self.cells[x][y] != 0:
            return Result(False, "Space is already filled.")
        
        # ok to proceed
        return Result(True)

    def place(self, x: int, y: int, value):
        '''Places a value at a cell'''

        self.cells[x][y] = value
        self.cur_move += 1
        self.history.insert(0, (x, y, value, self.score))
        self.add_log("move", f"Placed {value} in space ({x},{y}).")
        return Result(True)

    def undo(self):
        '''reverses the most recent move in the history'''

        last_move: tuple
        # if there are any moves to reverse
        if len(self.history):
            last_move = self.history.pop(0)
        else:
            return None
        # reverse the move, decriment last move, restore score, and remove value from x, y
        self.cur_move -= 1
        self.score = last_move[3]
        self.cells[last_move[0]][last_move[1]] = 0
        self.add_log("undo", f"Removed {last_move[2]} from ({last_move[0]},{last_move[1]})")
        return last_move

    def clear(self):
        '''reverses every move in the history'''
        if not len(self.history):
            return
        self.add_log("clear", "clearing history")
        while len(self.history):
            self.undo()

    def add_log(self, category: str, description):
        '''Add an entry to the game's log'''
        self.log.append(f"[{category}] {description}\n")    
    
    def level_up(self) -> Result:
        '''Attempt to premote the game board to the next level'''
        # make sure all cells are filled
        for row in self.cells:
            for cell in row:
                if cell == 0:
                    return Result(None, "All spaces must be filled before moving to the next level")
        
        # is premotion possible?
        if (self.level + 1) <= len(Game_loader.levels):
            # make a new game object based on this game, at the next higher level
            cls = Game_loader.levels[self.level + 1]
            # make new instance of the required type
            # the type will alsways be lvl2 or more, and take a lower level game as its argument
            new_game: Game = cls(self)
            new_game.add_log("level up", f"leveled up from level {self.level} to level {new_game.level}, with a score of {self.score}.")
            Game_loader.save_game(self, f"{self.player}")
            return Result(new_game, f"Premoted from level {self.level} to level {new_game.level}") 
        else:
            self.add_log("Game Finished", f"Game finished with a score of {self.score}")
            Game_loader.save_game(self, f"{self.player}")
            return Result(None, "Game is already at max level")


    def from_data(self, data: dict) -> None:
        '''Populate the object's atributes from a dictionary'''
        self.cells   = data["cells"]
        self.size    = data["size"]
        self.score   = data["score"]
        self.level   = data["level"]
        self.player  = data["player"]
        self.log     = data["log"]
        self.history = data["history"]
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


class Level1(Game):
    def __init__(self, player_name: str, size: int):
        super().__init__(size)
        self.level: int = 1
        self.player = player_name
        # add a header to the log
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


    def place(self, x: int, y: int, value: int = None) -> Result:
        # does the placement pass the basic checks?
        basic_checks = super().can_place(x, y, value)
        if not basic_checks.success():
            return basic_checks

        # check 3x3 area arround the move
        u: int = max(x - 1, 0)
        v: int = max(y - 1, 0)
        w: int = min(x + 1, self.size - 1)
        h: int = min(y + 1, self.size - 1)

        # look for predecessor in 3x3 area
        predecessor = None
        for i in range(u, w + 1):
            for j in range(v, h + 1):
                if self.cells[i][j] == value - 1:
                    predecessor = (abs(x-i), abs(y-j))

        if not predecessor:
            return Result(False, "Move must be a neighbor of its predececcor.")

        # make sure value is correct (ascending order)
        if not value:
            value = self.cur_move
            self.cur_move += 1
        elif value != self.cur_move:
            return Result(False, "Move's value must be 1 greater than its predecesor.")

        # make the move
        self.last_move = (x, y)
        placed: Result = super().place(x, y, value)

        # asses score for the move (is move place on a diagonal)
        dx, dy = predecessor
        if dx == dy:
            self.score += 1

        return placed
    

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
        self.player = base_game.player
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

    def place(self, x: int, y: int, value: int = None) -> Result:
        # does the placement pass the basic checks?
        basic_checks = super().can_place(x, y, value)
        if not basic_checks.success():
            return basic_checks

        # make sure number has not already been played
        if self.played[value]:
            return Result(False, "Each number may only be placed once.")

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
            return Result(False, "The number of the move and the number in the inner board must be on a straight line.")

        # make the move
        self.played[value] = True
        return super().place(x, y, value)

    def undo(self):
        undone_move = super().undo()
        # also update played[] for level 2
        if undone_move:
            self.played[undone_move[2]] = False

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
        game.add_log("Save", f"Game saved at {datetime.now()}")
        # save a json and log file
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
                obj.add_log("Load", f"game loaded at {datetime.now()}")
                return obj



if __name__ == "__main__":
    # used for testing, play the game on the terminal

    name: str = input("please enter your name: ")
    newGame: Game = Level1(name, 5)

    while True:
        # display board
        print(newGame)
        # take input
        in_str: str = input("enter your move 'x y value' (s=save, l=load, q=quit):")

        # parse input
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
        # make the move
        place_result: Result = newGame.place(int(x)-1, int(y)-1, int(val))

        # send feedback
        if not place_result.success():
            print(place_result)
        
        # check for level up
        lvl_up = newGame.level_up()
        if lvl_up.success():
            newGame = lvl_up.game_board()
        