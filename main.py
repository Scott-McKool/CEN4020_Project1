#!./venv/bin/python3
from json import load, dump
from random import randint
import playsound

class Move_result:
    '''The result of an attempted move on the game board, it is either a success or not, and has an acompanying decription'''
    data: tuple[bool, str]
    def __init__(self, success: bool, description: str = "Description missing."):
        self.data = (success, description)

    def success(self) -> bool:
        '''Was the move successfull'''
        return self.data[0]
    
    def description(self) -> str:
        '''The description of the move'''
        return self.data[1] or "Description missing."

    def __str__(self):
        if self.success():
            playsound.playsound('C:/Users/duxed/OneDrive/Documents/CODE/CEN4020_Project1/correct.mp3', block=False)
            return self.description()
        
        if not self.success():
            playsound.playsound('C:/Users/duxed/OneDrive/Documents/CODE/CEN4020_Project1/wrong.mp3', block=False)
            return f"unsuccessfull move: {self.data[1]}"

class Game:
    cells: list[list[int]]
    size : int
    score: int
    level: int
    def __init__(self, size: int):
        self.level = None
        self.score = 0
        self.size = size
        # init cell values 
        self.cells = [[0]*size for _ in range(size)]
    
    def place(self, x: int, y: int, value: int) -> Move_result:
        '''Attempt to place a value at a given coordinate within the rules of the game. x and y are index values'''
        # make sure coords are in-bounds
        if x >= self.size or y >= self.size or x < 0 or y < 0:
            return Move_result(False, "Given coordinates are out of bounds.")
        
        # make sure space in unnoccupied
        if self.cells[x][y] != 0:
            return Move_result(False, "Space is already filled.")
        
        # ok to proceed
        return Move_result(True)
        
    def from_data(self, data: dict) -> None:
        '''Populate the object's atributes from a dictionary'''
        self.cells = data["cells"]
        self.size  = data["size"]
        self.score = data["score"]
        self.level = data["level"]

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
        self.cur_move: int = 2
        # choose location for '1'
        rand_x: int = randint(0, self.size - 1)
        rand_y: int = randint(0, self.size - 1)
        self.cells[rand_x][rand_y] = 1
        self.last_move = (rand_x, rand_y)


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

        # make the move
        if not value:
            value = self.cur_move
            self.cur_move += 1
        elif value != self.cur_move:
            return Move_result(False, "Move's value must be 1 greater than its predecesor.")

        self.cells[x][y] = value
        self.last_move = (x, y)
        return Move_result(True)

    def from_data(self, data) -> None:
        self.cur_move  = data["cur_move"]
        self.last_move = data["last_move"]
        super().from_data(data)


class Game_loader():
    levels: dict = {
        1 : Level1
    }
        
    def save_game(game: Game, name: str):
        '''Saves a provided game object to a json text file with the provided name'''
        with open(f"saved_games/{name}", "wt") as outfile:
            dump(game.__dict__, outfile, indent=4)

    def load_game(name: str) -> Game:
        '''loads a game board of the appropriate type from a json file'''
        obj: Game
        with open(f"saved_games/{name}") as infile:
            data = load(infile)
        
        for key, cls in Game_loader.levels.items():
            if data["level"] == key:
                # make new instance of the required type
                obj = cls.__new__(cls)
                # populate the required data
                obj.from_data(data)
                return obj



if __name__ == "__main__":
    newGame: Game = Level1(10)

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

        x, y = in_str.split(" ")
        did_place: Move_result = newGame.place(int(x)-1, int(y)-1)

        if not did_place.success():
            print(did_place)
        