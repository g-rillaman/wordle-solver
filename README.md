# Wordle Solver

Short script used to play (and hopefully beat) Wordle. 

## Approach
A list of possible answers is able to be found in the game's source code. `answer_space.txt` contains this and is used as our starting space for a new game. Our program aims to reduce this space by as many words as possible each guess, with the result of each being reflected in the updated vocabulary list (remaining possible answers). Note: the possible guesses - that cannot be answers - are also included in this repo for completness.

## Current version and future 
Currently the program requires input from the user to read in the result of each guessed word. The end idea is to have this by automated, either by a Wordle API (not sure there is one), a Selenium webdriver, or using PyAutoGui.
