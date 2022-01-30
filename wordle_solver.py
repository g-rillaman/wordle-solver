# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 15:34:33 2022

@author: LReynolds
"""

def read_in_vocabulary():
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
    
class WordleState:
    guesses = 1
    
    def __init__(self, vocabulary, current_guess):
        self.vocabulary = vocabulary
        self.current_guess = current_guess
        self.next_guess = None
        self.guess_result = []
        print(self)
    
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
        next_best_guess = ''
        pruned_vocabulary = self.vocabulary
        
        for guess_word in self.vocabulary:
            guess_vocabulary = [word for word in self.vocabulary
                              if not self.words_share_letters(word, guess_word)]
            if len(guess_vocabulary) < len(pruned_vocabulary):
                #print("Changed")
                next_best_guess = guess_word
                pruned_vocabulary = guess_vocabulary
        
        self.current_guess = next_best_guess
    
    @staticmethod
    def words_share_letters(word_1, word_2):
        for letter in word_1:
            if letter in word_2:
                return True
            
        return False
    
    def input_guess_result(self):
        """Take user input of guess result."""
        print(f"The current guess is {self.current_guess}.")
        guess_result = []
        for idx, letter in enumerate(self.current_guess):
            colour = input(f"Enter the colour of {letter} at {idx}: ")
            letter_state = LetterGuess(idx, letter, colour)
            guess_result.append(letter_state)
        
        self.guess_result = guess_result
        
        return WordleState(self.prune_vocabulary(), self.current_guess)
    
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
    
    def __repr__(self):
        return f"""
    WordleState:
        Current guess : {self.current_guess}
        Next guess : {self.next_guess}
        Vocab Length : {len(self.vocabulary)}
        self.next_guess = None
        self.guess_result = []
        """
                
 
class LetterGuess():
    def __init__(self, position, letter, colour):
        self.position = position  # 0-indexed
        self.letter = letter
        self.colour = colour


if __name__ == "__main__":
    answer_space, _ = read_in_vocabulary()
    state = WordleState(answer_space, 'arise')
    while WordleState.guesses < 7:
        state.get_best_guess()
        state = state.input_guess_result()
        WordleState.guesses += 1
    