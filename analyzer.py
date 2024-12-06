import pandas as pd
from collections import Counter
from itertools import permutations

class Analyzer:
    def __init__(self, game):
        """
        Initializes the Analyzer with the results of a Game object.

        Parameters:
        game (Game): An instance of the Game class containing the results to analyze.

        Raises:
        ValueError: If the provided game parameter is not an instance of Game.
        """
        if not isinstance(game, Game):
            raise ValueError("Input must be a Game object.")
        
        self.game = game
        self.results = self.game.show_results()  # Store the game results for analysis

    def jackpot(self):
        """
        Computes the number of jackpots in the game results.

        A jackpot is defined as all faces rolled being the same in a given roll.

        Returns:
        int: The number of jackpots found in the game results.
        """
        jackpot_count = 0
        for roll in self.results.itertuples(index=True):
            if len(set(roll[1:])) == 1:  # Check if all rolled faces are the same
                jackpot_count += 1
        return jackpot_count

    def face_counts_per_roll(self, face):
        """
        Computes how many times a given face is rolled in each event.

        Parameters:
        face (str): The face value to count (must be in the set of faces).

        Returns:
        pd.DataFrame: A DataFrame with an index of roll number and counts for the specified face.
        """
        if face not in self.results.columns:
            raise ValueError(f"Face '{face}' is not a valid face.")

        counts = self.results.apply(lambda x: (x == face).sum(), axis=1)
        return pd.DataFrame({'Roll Number': self.results.index, face: counts})

    def combo_count(self):
        """
        Computes the distinct combinations of faces rolled, along with their counts.

        Returns:
        pd.DataFrame: A DataFrame with a MultiIndex of distinct combinations and their associated counts.
        """
        combos = []
        for roll in self.results.itertuples(index=True):
            combos.append(tuple(sorted(roll[1:])))  # Sort to ignore order

        combo_counts = Counter(combos)
        combo_df = pd.Series(combo_counts).reset_index(name='Count').rename(columns={'index': 'Combination'})
        combo_df.index.names = ['Combination']
        return combo_df

    def permutation_count(self):
        """
        Computes the distinct permutations of faces rolled, along with their counts.

        Returns:
        pd.DataFrame: A DataFrame with a MultiIndex of distinct permutations and their associated counts.
        """
        perms = []
        for roll in self.results.itertuples(index=True):
            perms.extend(permutations(roll[1:]))  # Generate all permutations for the roll

        perm_counts = Counter(perms)
        perm_df = pd.DataFrame.from_dict(perm_counts, orient='index', columns=['Count'])
        perm_df.index.names = ['Permutation']
        return perm_df
