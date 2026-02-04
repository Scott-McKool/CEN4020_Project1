#!./venv/bin/python3
from json import load, dump
from random import randint

class Result:
    '''The result of attempting a given action, it is either successfull or not, and includes a text description of the result'''
    data: tuple[bool, str]
    def __init__(self, success: bool, description: str = "Description missing."):
        self.data = (success, description)

    def success(self) -> bool:
        '''Does the result represent a success (true if yes, false if no)'''
        return self.data[0]
    
    def description(self) -> str:
        '''The description of the result'''
        return self.data[1] or "Description missing."
    
    def __str__(self):
        if self.success():
            return f"Successful: {self.description()}"
        
        if not self.success():
            return f"Unsuccessfull: {self.description()}"


class Game:
    cells: list[list[int]]
    size : int
    score: int
    level: int
    cur_move: int
    def __init__(self, size: int):
        self.cur_move = 2
        self.level = None
        self.size = size
        self.score = 0
        # init cell values 
        self.cells = [[0]*size for _ in range(size)]
    
    def place(self, x: int, y: int, value: int) -> Result:
        '''Attempt to place a value at a given coordinate within the rules of the game. x and y are index values'''
        # make sure coords are in-bounds
        if x >= self.size or y >= self.size or x < 0 or y < 0:
            return Result(False, "Given coordinates are out of bounds.")
        
        # make sure space in unnoccupied
        if self.cells[x][y] != 0:
            return Result(False, "Space is already filled.")
        
        # ok to proceed
        return Result(True)
        
    def from_data(self, data: dict) -> None:
        '''Populate the object's atributes from a dictionary'''
        self.cells = data["cells"]
        self.size  = data["size"]
        self.score = data["score"]
        self.level = data["level"]
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
    def __init__(self, size: int):
        super().__init__(size)
        self.level: int = 1

        ### initialize board for play
        # choose location for '1'
        rand_x: int = randint(0, self.size - 1)
        rand_y: int = randint(0, self.size - 1)
        self.cells[rand_x][rand_y] = 1
        self.last_move = (rand_x, rand_y)


    def place(self, x: int, y: int, value: int = None) -> Result:
        # does the placement pass the basic checks?
        basic_checks = super().place(x, y, value)
        if not basic_checks.success():
            return basic_checks

        # make sure space is the neighbor of its predecessor
        dx = abs(self.last_move[0] - x)
        dy = abs(self.last_move[1] - y)

        if dx > 1 or dy > 1:
            return Result(False, "Move must be a neighbor of its predececcor.")
        
        # asses score for the move (is move place on a diagonal)
        if dx == dy:
            self.score += 1

        # make sure value is correct (ascending order)
        if not value:
            value = self.cur_move
            self.cur_move += 1
        elif value != self.cur_move:
            return Result(False, "Move's value must be 1 greater than its predecesor.")

        # make the move
        self.cells[x][y] = value
        self.last_move = (x, y)
        return Result(True)

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
        # carry over the values from the level 1 board
        for y in range(0, base_game.size):
            for x in range(0, base_game.size):
                self.cells[x+1][y+1] = base_game.cells[x][y]


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
        basic_checks = super().place(x, y, value)
        if not basic_checks.success():
            return basic_checks

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
        self.cells[x][y] = value
        return Result(True)

    def from_data(self, data) -> None:
        super().from_data(data)

class Game_loader():
    levels: dict = {
        1 : Level1,
        2 : Level2
    }
        
    def save_game(game: Game, name: str):
        '''Saves a provided game object to a json text file with the provided name'''
        with open(f"saved_games/{name}.json", "wt") as outfile:
            dump(game.__dict__, outfile, indent=4)

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
    newGame: Game = Level1(5)

    while True:

        print(newGame)
        in_str: str = input("enter your move 'x y' (s=save, l=load, q=quit):")

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
        did_place: Result = newGame.place(int(x)-1, int(y)-1, int(val))

        if not did_place.success():
            print(did_place)
        