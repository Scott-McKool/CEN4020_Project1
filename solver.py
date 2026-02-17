#!./venv/bin/python
# this file is for a solver for game boards
from main import Game, Result, Err, OK, Level1
from time import time

class Move():
    x: int
    y: int
    val : int

    def __init__(self, x: int, y: int, val: int):
        self.x = x
        self.y = y
        self.val = val

    def __str__(self):
        return f"Move at ({self.x},{self.y}) with value {self.val}"

class Solver():

    def get_moves(game: Game) -> list[Move]:
        '''Returns a list of all legal moves on the given board'''

        all_moves: list[Move] = []

        # for each possible move that could be made
        for x, row in enumerate(game.cells):
            for y, cell in enumerate(row):

                # try to make the move
                mv: Move = Move(x, y, game.cur_move)
                try_place: Result = game.place(mv.x, mv.y, mv.val)

                if try_place.success():    
                    all_moves.append(mv)
                    game.undo()
        
        return all_moves


    def most_constrained_move(game: Game) -> Move:
        '''Returns the legal move on the game board that has the fewest available moves after it'''

        fewest: int = 1e99
        best: Move = None

        # of all the legal moves
        mv : Move
        for mv in Solver.get_moves(game):

            # calculate the number of child moves for this potential move
            game.place(mv.x, mv.y, mv.val)
            legal_moves = len(Solver.get_moves(game))
            game.undo()

            # if this move is the new best (has fewest child moves)
            if legal_moves < fewest:
                fewest = legal_moves
                best = mv

        return best


    def dfs(game: Game, deadline: int) -> Result:
        '''use depth fisrt search to look for a combination of moves that leads to a finished board. returns either a finished game board or None'''
        
        # check for win
        if game.is_filled():
            return OK(game)

        
        while True:
            # check for time
            if time() > deadline:
                return Err("Solver ran out of time.")

            # get the next move
            mv: Move = Solver.most_constrained_move(game)
            if mv is None:
                return Err("Board has no valid solution.")
            
            # make the move
            game.place(mv.x, mv.y, mv.val)

            # do dfs
            did_solve: Result = Solver.dfs(game, deadline)
            if did_solve.success():
                return did_solve    # propigate up success
            else:
                game.undo()         # try again with a different move
                continue

        
    def solve(game, time_limit: int = 1):
        '''Attempts to solve a given game board, will either return the filled game board or None. will only run for time_limit seconds'''

        return Solver.dfs(game, time() + time_limit)

                    
def test_boards(size: int = 5) -> list[Game]:

    all_games = []

    for i in range(size):
        for j in range(size):
            newGame = Level1("test", size)
            for x, row in enumerate(newGame.cells):
                for y, cell in enumerate(row):
                    newGame.cells[x][y] = 0
            newGame.cells[i][j] = 1
            all_games.append(newGame)

    return all_games


if __name__ == "__main__":

    for game in test_boards(5):

        print(game)

        did_solve: Result = Solver.solve(game)
        print(did_solve)
        print(did_solve.obj())

        assert(did_solve.success() == True)