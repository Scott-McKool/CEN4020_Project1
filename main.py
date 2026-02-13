#!./venv/bin/python3
from __future__ import annotations
from datetime import datetime
from datetime import datetime
from json import load, dump
from random import randint

class Result:
    '''The result of attempting an action that is not guarenteed.\n
    .success() returns if the attempted action was successfull.\n
    .obj() returns either an object (if the action resuts in an object) or none.\n
    .description() returns a string that is a description of the result.'''
    data        : tuple[object, str]
    successful  : bool

    def __init__(self, obj: object, description: str = "Description missing"):
        self.data = (obj, description)

    def success(self) -> bool:
        '''Did the attempted action succeed?'''
        return self.successful

    def obj(self) -> object:
        '''The returned object'''
        return self.data[0]
        
    def description(self) -> str:
        '''The description of the result'''
        return self.data[1] or "Description missing."
    
    def __str__(self):
        if self.success():
            return f"Successful: {self.description()}"
        
        if not self.success():
            return f"Unsuccessful: {self.description()}"

class Err(Result):
    '''Error variant of a result.'''
    def __init__(self, description = "Description missing"):
        super().__init__(None, description)
        self.successful = False

class OK(Result):
    ''''Successful variant of result.'''
    def __init__(self, obj = None, description = "Description missing"):
        super().__init__(obj, description)
        self.successful = True



class Game:
    cells: list[list[int]]
    size : int
    level: int
    log  : list[str]
    player      : str
    cur_move    : int
    history     : list[tuple[int, int, int]]
    base_score  : int

    def __init__(self, size: int):
        self.size = size
        self.level = None
        self.cur_move = 2
        self.base_score = 0
        self.log = list()
        self.history = list()
        # init cell values 
        self.cells = [[0]*size for _ in range(size)]
        self.diagflag = False
        self.next_number = 2 # L1 begins 
        self.move_stack = [] # undo
        self.one_p = None # initial positions of x and y
        self.log = []
    
    def find_value(self, value: int) -> Result:
        '''Given a value, returns the (x,y) coordinate of the instances of the value'''

        # compose tuple of coordinates of matches
        found = tuple([
            (x, y)
            for x, row in enumerate(self.cells)
            for y, cell in enumerate(row)
            if cell == value
        ])

        if len(found) == 0:
            return Err("Value not found.")
        
        return OK(found)

    def can_place(self, x: int, y: int, value: int) -> Result:
        '''Checks if it is valid to place a value at a given coordinate within the rules of the game. x and y are index values'''

        # make sure coords are in-bounds
        if x >= self.size or y >= self.size or x < 0 or y < 0:
            return Err("Given coordinates are out of bounds.")
        
        # make sure space in unnoccupied
        if self.cells[x][y] != 0:
            return Err("Space is already filled.")
        
        # ok to proceed
        return OK()

    def is_filled(self) -> bool:
        '''Returns true if every cell on the board is filled'''

        for row in self.cells:
            for cell in row:
                if cell == 0:
                    return False
        return True

    def score(self) -> int:
        return self.base_score

    def place(self, x: int, y: int, value):
        '''Places a value at a cell'''

        can_place: Result = self.can_place(x, y, value)
        if not can_place.success():
            return can_place      

        self.cells[x][y] = value
        self.cur_move += 1
        self.history.append((x, y, value))
        self.add_log("move", f"Placed {value} in space ({x},{y}).")
        return OK()

    def undo(self) -> Result:
        '''reverses the most recent move in the history'''

        last_move: tuple
        # if there are any moves to reverse
        if len(self.history):
            last_move = self.history.pop()
        else:
            return Err("No Moves to undo.")
        
        # reverse the move, decriment last move, restore score, and remove value from x, y
        self.cur_move -= 1
        self.cells[last_move[0]][last_move[1]] = 0
        self.add_log("undo", f"Removed {last_move[2]} from ({last_move[0]},{last_move[1]})")
        return OK(last_move)

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
        if not self.is_filled():
            return Err("All spaces must be filled before moving to the next level")
        
        # is premotion possible?
        if (self.level + 1) <= len(Game_loader.levels):
            # make a new game object based on this game, at the next higher level
            cls = Game_loader.levels[self.level + 1]
            # make new instance of the required type
            # the type will alsways be lvl2 or more, and take a lower level game as its argument
            new_game: Game = cls(self)
            new_game.add_log("level up", f"leveled up from level {self.level} to level {new_game.level}, with a score of {self.score()}.")
            Game_loader.save_game(self, f"{self.player}")
            return OK(new_game, f"Premoted from level {self.level} to level {new_game.level}") 
        else:
            self.add_log("Game Finished", f"Game finished with a score of {self.score()}")
            Game_loader.save_game(self, f"{self.player}")
            return Err("Game is already at max level")


    def from_data(self, data: dict) -> None:
        '''Populate the object's atributes from a dictionary'''

        self.cells   = data["cells"]
        self.size    = data["size"]
        self.level   = data["level"]
        self.player  = data["player"]
        self.log     = data["log"]
        self.history = data["history"]
        self.cur_move  = data["cur_move"]
        self.base_score   = data["base_score"]

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
        result += f"\n\nScore: {self.score()}"
        
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
        if self.level == 2:
            self.played[self.cells[prev["x"]][prev["y"]]] = False
        self.set(prev["x"], prev["y"], 0)
        self.score = prev["prev_score"]
        self.cur_move = prev["next"]
        if self.level == 1:
            self.last_move = prev["last_move"]

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
            self.last_move = self.one_p

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
            self.played = [False] * (2 * (self.size + self.size))
            return Move_result(True, "Outer grid cleared. ")
        
        # 
        return Move_result(False, f"Uknown Level --> {self.level} not available")


class Level1(Game):
    def __init__(self, player_name: str, size: int):
        super().__init__(size)
        self.move_stack = []
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

    def can_place(self, x: int, y: int, value: int):
        '''can the value be placed at (x,y) according to the game rules?'''

        # does the placement pass the basic checks?
        basic_checks = super().can_place(x, y, value)
        if not basic_checks.success():
            return basic_checks
        
        # check if predecessor is on the board
        found_pred: Result = self.find_value(value - 1)

        pred_pos: tuple
        if found_pred.success():
            pred_pos = found_pred.obj()
        else:
            return found_pred
        
        # check if predecessor is a neighbor
        px, py = pred_pos[0]
        dx = abs(x - px)
        dy = abs(y - py)

        if dx > 1 or dy > 1:
            return Err("Move must be a neighbor of its predecessor")

        # make sure value is correct (ascending order)
        if value:
            if value != self.cur_move:
                return Err("Move's value must be 1 greater than its predecesor.")

        # ok to proceed
        return OK()

    def place(self, x: int, y: int, value: int = None) -> Result:
        '''Attempt to place the value [value] at coordinates ([x], [y])'''

        if not value:
            value = self.cur_move

        did_place: Result = super().place(x, y, value)
        if not did_place.success():
            return did_place

        return did_place


    def score(self) -> int:
        '''calculates and returns the score of the game board'''

        score = self.base_score

        # look for the one position
        cur_pos: tuple[int, int]
        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                if cell == 1:
                    cur_pos = (x, y)

        # starting from the one position, proceed up the numbers while keeping score
        value: int = 1
        while True:
            found_next: Result = self.find_value(value + 1)
            if found_next.success():
                # check if next value is on diagonal
                x, y = cur_pos
                px, py = found_next.obj()[0]

                dx = abs(x - px)
                dy = abs(y - py)
                # add score for diagonal
                if dx == dy:
                    score += 1

                # incriment to next value
                cur_pos = (px, py)
                value += 1
            else:
                return score    

    def from_data(self, data) -> None:
        super().from_data(data)


class Level2(Game):
    def __init__(self, base_game: Level1):
        # a level2 board is initialized from a level1 board, but with the outer ring of spaces
        size = base_game.size + 2
        super().__init__(size)
        # inherit values from the level1 board
        self.base_score = base_game.score()
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

    def can_place(self, x, y, value):
        '''can the value be placed at (x,y) according to the game rules?'''

        # does the placement pass the basic checks?
        basic_checks: Result = super().can_place(x, y, value)
        if not basic_checks.success():
            return basic_checks
        
        # make sure number has not already been played
        if self.played[value] == True:
            return Err("Each number may only be placed once.")

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
            return Err("The number of the move must be on a straight line with the same number in the inner board.")
        
        return OK()


    def place(self, x: int, y: int, value: int = None) -> Result:
        '''Attempt to place the value [value] at coordinates ([x], [y])'''

        if not value:
            value = self.cur_move

        did_place: Result = super().place(x, y, value)
        if not did_place.success():
            return did_place

        # make the move
        self.played[value] = True
        return did_place

    def score(self) -> int:
        return self.base_score

    def undo(self) -> Result:

        # return result if failed
        did_undo = super().undo()
        if not did_undo.success():
            return did_undo
        
        # update played[] for level 2 functionality
        undone_move = did_undo.obj()
        self.played[undone_move[2]] = False

    def from_data(self, data) -> None:
        super().from_data(data)
        self.played = data["played"]
        

class Level3(Game):

    def __init__(self, base_game: Level1):
        # a level2 board is initialized from a level1 board, but with the outer ring of spaces
        super().__init__(base_game.size)
        # inherit values from the level1 board
        self.base_score = base_game.score()
        self.level = 3
        self.player = base_game.player
        self.log = base_game.log
        # carry over the values from the level 2 board
        self.cells = base_game.cells
        for y in range(1, base_game.size - 1):
            for x in range(1, base_game.size -1 ):
                if self.cells[x][y] != 1:
                    self.cells[x][y] = 0

    def can_place(self, x, y, value):
        '''can the value be placed at (x,y) according to the game rules?'''

        # does the placement pass the basic checks?
        basic_checks: Result = super().can_place(x, y, value)
        if not basic_checks.success():
            return basic_checks
        
        # do level 1 check for predecesor

        # make sure value is correct (ascending order)
        if value:
            if value != self.cur_move:
                return Err("Move's value must be 1 greater than its predecesor.")

        # check if predecessor is on the board
        found_pred: Result = self.find_value(value - 1)

        coords: tuple
        if found_pred.success():
            coords = found_pred.obj()
        else:
            return found_pred
        
        found = False
        for coord in coords:

            # check if predecessor is a neighbor
            px, py = coord
            dx = abs(x - px)
            dy = abs(y - py)

            if dx <= 1 and dy <= 1:
                found = True
                break
        
        if not found:
            return Err("Move must be a neighbor of its predecessor")

            
        # do level 2 check for line

        # check up, down, left, and rightmost cells
        to_check: list[tuple[int, int]] = []

        to_check.append((0, y))             # leftmost
        to_check.append((self.size-1, y))   # rightmost
        to_check.append((x, 0))             # upmost
        to_check.append((x, self.size-1))   # downmost

        # if on the main diagonal (top left to bottom right)
        if x == y:
            # add top left and top right
            to_check.append((0, 0))
            to_check.append((self.size-1, self.size-1))

        # if on the antidiagonal (top right to bottom left)
        if (self.size - 1 - x) == y:
            # add top right and bottom left
            to_check.append((self.size-1, 0))
            to_check.append((0, self.size-1))

        # check the relevent cells for a match
        found = False
        for coord in to_check:
            px, py = coord
            if value == self.cells[px][py]:
                found = True
                break

        if not found:
            return Err("The number of the move must be on a straight line with the same number in the outer ring.")

        return OK()
    
    def place(self, x: int, y: int, value: int = None) -> Result:
        '''Attempt to place the value [value] at coordinates ([x], [y])'''

        if not value:
            value = self.cur_move

        did_place: Result = super().place(x, y, value)
        if not did_place.success():
            return did_place

        # make the move
        return did_place


class Game_loader():
    levels: dict = {
        1 : Level1,
        2 : Level2,
        3 : Level3,
    }
        
    def save_game(game: Game, name: str):
        '''Saves a provided game object to a json text file with the provided name'''
        game.add_log("Save", f"Game saved at {datetime.now()}")
        # save a json and log file
        with open(f"saved_games/{name}.json", "wt") as outfile:
            dump(game.__dict__, outfile, indent=4)
        with open(f"saved_games/{name}.log", "wt") as outfile:
            outfile.writelines(game.log)

    def load_game(name: str) -> Result:
        '''loads a game board of the appropriate type from a json file'''
        obj: Game
        try:
            with open(f"saved_games/{name}.json") as infile:
                data = load(infile)
        except FileNotFoundError as e:
            return Err(f"{e}")
        
        for key, cls in Game_loader.levels.items():
            if data["level"] == key:
                # make new instance of the required type
                obj = cls.__new__(cls)
                # populate the required data
                obj.from_data(data)
                obj.add_log("Load", f"game loaded at {datetime.now()}")
                return OK(obj)


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

#         if in_str == "s":
#             in_str = input("Choose a filename for your game: ")
#             Game_loader.save_game(newGame, in_str)
#             continue

        if in_str == "l":
            in_str = input("type the game file to load: ")
            did_load: Result = Game_loader.load_game(in_str)
            if did_load.success():
                newGame = did_load.obj()
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
            newGame = lvl_up.obj()
        