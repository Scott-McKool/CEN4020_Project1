#!./venv/bin/python
# this file is for a solver for game boards
from result import Result, Err, OK
from game import Game
from copy import deepcopy
from time import time

class Move():
    '''Object for storing data relevent to a move on the game board'''
    x: int
    y: int
    val : int

    def __init__(self, x: int, y: int, val: int):
        self.x = x
        self.y = y
        self.val = val

    def __hash__(self):
        return hash(tuple([self.x, self.y, self.val]))

    def __str__(self):
        return f"Move at ({self.x},{self.y}) with value {self.val}"

class Solver():

    def get_moves(game: Game, cache: dict = dict()) -> list[Move]:
        '''Returns a list of all legal moves on the given board'''

        # check the cache
        if hash(game) in cache.keys():
            return cache[hash(game)]

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
        
        # add to cache
        cache[hash(game)] = all_moves

        return all_moves
    

    def count_child_moves(game: Game, mv: Move, cache: dict = dict()) -> int:
        '''Returns the number of legal moves that will be available if a given move is made on the game board'''

        # check the cache
        if hash(game) + hash(mv) in cache.keys():
            return cache[hash(game) + hash(mv)]

        game.place(mv.x, mv.y, mv.val)  # simulate placing move
        legal_moves = len(Solver.get_moves(game)) # count legal moves
        game.undo() # undo move

        # add to cache
        cache[hash(game) + hash(mv)] = legal_moves

        return legal_moves


    def dfs(game: Game, deadline: int, cache: dict) -> Result:
        '''use depth fisrt search to look for a combination of moves that leads to a finished board. returns either a finished game board or None'''

        # check for win
        if game.is_filled():
            return OK(game)

        # check the cache
        if hash(game) in cache.keys():
            return cache[hash(game)]
        
        # get all possible moves
        moves: list[Move] = Solver.get_moves(game)

        # sort the moves from least children to most children (most constrained to least constrained)
        moves = sorted(
            moves,
            key=lambda mv: Solver.count_child_moves(game, mv)
        )
        # for each move
        mv: Move
        for mv in moves:
            
            # check for deadline
            if time() > deadline:
                return Err("Solver ran out of time")
            
            # test out the move
            game.place(mv.x, mv.y, mv.val)

            # call dfs recursively, take time off the deadline to limit time spent on incorrect branches
            did_solve: Result = Solver.dfs(game, deadline, cache)

            # add to cache
            cache[hash(game)] = did_solve

            if did_solve.success():
                return did_solve    # propigate up success
            else:
                game.undo()         # try again with a different move
                continue

        return Err("No valid solution")

        
    def solve(game, time_limit: int = 1):
        '''Attempts to solve a given game board, will either return the filled game board or None. will only run for time_limit seconds'''

        # create a copy of game, set the time limit, and then solve the copy and return it.
        return Solver.dfs(deepcopy(game), time() + time_limit, dict())
