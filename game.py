import pandas as pd

class Game:
    def __init__(self, dice):
        if not isinstance(dice, list) or not all(isinstance(d, Die) for d in dice):
            raise TypeError("Input must be a list of Die objects.")
        
        if len(dice) < 2:
            raise ValueError("At least two dice are required for the game.")
        
        face_count = dice[0].faces  # Assuming 'faces' is an attribute of Die
        if not all(d.faces == face_count for d in dice):
            raise ValueError("All dice must have the same number of faces.")
        
        self.dice = dice
        self._last_play_results = None # To store results of the most recent play

    def play(self, rolls):
        # Validate the number of rolls
        if rolls < 1:
            raise ValueError("Number of rolls must be at least 1.")

        # Roll all dice for the specified number of times
        results = {}
        for i, die in enumerate(self.dice):
            results[i] = die.roll(rolls)

        # Create a DataFrame to store the results in wide format
        self._last_play_results = pd.DataFrame(results)
        self._last_play_results.index.name = "Roll Number"

    def show_results(self):
        # Return a copy of the last play results
        if self._last_play_results is None:
            raise ValueError("No results available. Please play the game first.")
        return self._last_play_results.copy()

    def get_results(self, form='wide'):
        # Validate the form parameter
        if form not in ['wide', 'narrow']:
            raise ValueError("Invalid option for form. Choose 'wide' or 'narrow'.")

        if form == 'wide':
            return self.show_results()

        # Convert to narrow form (MultiIndex)
        narrow_results = self._last_play_results.stack().reset_index()
        narrow_results.columns = ['Roll Number', 'Die Number', 'Outcome']
        narrow_results.set_index(['Roll Number', 'Die Number'], inplace=True)
        return narrow_results