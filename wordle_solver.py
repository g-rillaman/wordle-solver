# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 15:34:33 2022

@author: LReynolds
"""
class WordleState:
    def __init__(self):
        self.answer_space, self.guess_space = self.read_in_vocabulary()
        self.vocabulary = self.answer_space
        self.guess = None
        self.guess_result = []
    
    def read_in_vocabulary(self):
        """
        Return list of vocabulary words from text file.
    
        Returns
        -------
        answer_space : List[str]
            List of possible answers.
        guess_space : List[str]
            List of possible answers.
        """
        answer_space = []
        guess_space = []
        
        with open("answer_space.txt", 'r', newline='\n') as word_file:
            for word in word_file:
                answer_space.append(word.strip())
        
        with open("guess_space.txt", 'r', newline='\n') as word_file:
            for word in word_file:
                guess_space.append(word.strip())
                
        return answer_space, guess_space
    
    def is_guess_correct(self):
        """Return True if the guess was the correct word, False otherwise."""
        for letter_state in self.guess_result:
            if letter_state.colour != 'g':
                return False
        
        return True
    
    def get_best_guess(self):
        """Return a guess word based on current vocabulary.
        
        The best guess word is defined as the word which reduces the
        vocaublary by the most amount if all the letters are grey.
        
        Returns
        -------
        best_guess : str
            The word calculated as the next best guess.
        pruned_vocabulary : str
            The potential vocabulary list if all letters of best_guess show as
            grey. If this occurs, the answer is contained in here.
        """        
        best_guess = ''
        pruned_vocabulary = self.vocabulary
        
        for guess_word in self.vocabulary:
            guess_vocabulary = [word for word in self.vocabulary
                              if not self.words_share_letters(word, guess_word)]
            if len(guess_vocabulary) < len(pruned_vocabulary):
                #print("Changed")
                best_guess = guess_word
                pruned_vocabulary = guess_vocabulary
        
        return best_guess, pruned_vocabulary
    
    @staticmethod
    def words_share_letters(word_1, word_2):
        for letter in word_1:
            if letter in word_2:
                return True
            
        return False
    
    def input_guess_result(self):
        guess_result = []
        for idx, letter in enumerate(self.guess):
            colour = input(f"Enter the colour of {letter} at {idx}: ")
            letter_state = LetterGuess(idx, letter, colour)
            guess_result.append(letter_state)
        
        return guess_result
    
    def prune_vocabulary(self):
        """Return new vocabulary based on the previous guess pattern."""
        new_vocab = self.vocabulary
        
        for letter_state in self.guess_result:
            if letter_state.colour == 'x':
                new_vocab = [word for word in new_vocab
                             if letter_state.letter not in word]
            elif letter_state.colour == 'y':
                new_vocab = [word for word in new_vocab
                             if letter_state.letter in word]
            elif letter_state.colour == 'g':
                new_vocab = [word for word in new_vocab
                             if letter_state.letter == word[letter_state.position]]
        
        return new_vocab
                
 
class LetterGuess():
    def __init__(self, position, letter, colour):
        self.position = position  # 0-indexed
        self.letter = letter
        self.colour = colour


if __name__ == "__main__":
    solver = WordleState()
    
    for i in range(6):
        print(f"Turn {i}")
        solver.guess, _ = solver.get_best_guess()
        print(f"Best guess is {solver.guess}")
        solver.guess_result = solver.input_guess_result()
        if solver.solved:
            print(f"The answer is {solver.guess}!")
            break
        solver.vocabulary = solver.prune_vocabulary()
    