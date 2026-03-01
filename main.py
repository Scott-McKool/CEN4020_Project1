#!./venv/bin/python3
from __future__ import annotations
from datetime import datetime
from json import load, dump
from random import randint
from result import Result, Err, OK
from game import Game, Level1, Level2, Level3, Game_loader




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
        