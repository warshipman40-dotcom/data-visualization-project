from random import randint
import pygal
import os
class Die():
    """A class that represents a single die"""
    def __init__(self, num_sides=6):
        """Default a six sided die"""
        self.num_sides = num_sides
        

    def roll(self):
        """Returns a single random value between 1 and number of sides."""
        return randint(1, self.num_sides)

    def roll_dice(self, num_rolls):
        self.num_rolls = num_rolls
        """Rolls a random number of rolls"""
        results = []
        #this line will roll the dice a certain number of rolls
        for roll in range(num_rolls):
            #this line will store the rolls in a list 
            cur_roll = self.roll()
            results.append(cur_roll)
        return results
    
    def get_frequencies(self, results):
        """Returns the frequency of value occurences"""
        frequencies = []
        max_result = self.num_sides
        for value in range(1, max_result + 1):
            frequencyOfValue = results.count(value)
            frequencies.append(frequencyOfValue)
        return frequencies
    
    def create_histogram(self, results, title = "Dice roll results",  filename = r"C:\Users\warsh\Downloads\python_work\Data Visualization\Hist.svg"):
        frequencies = self.get_frequencies(results)
        hist = pygal.Bar()
        hist.title = f"Results of rolling a {self.num_sides} sided die {self.num_rolls} times"
        hist.x_labels = list(range(1, self.num_sides + 1))
        hist.x_title = "Results"
        hist.y_title = "Frequencies"
        #this ensures the bar has the height of the value in frequencies for each
        hist.add("D6 Dice", frequencies)
        hist.render_to_file(filename)
        os.startfile(filename)