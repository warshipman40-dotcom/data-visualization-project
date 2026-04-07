#individual dice class
from random import randint
import pygal
import matplotlib.pyplot as plt
import mplcursors as mpl
import tkinter as tk
from tkinter import Tk
from tkinter import messagebox
from tkinter import filedialog
from pathlib import Path
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
        #results will store every roll that occurs
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
        #calculates expected results for a number of dice rolls based on the number of dice sides
        expected_result = round(self.num_rolls / self.num_sides, 3)        
        #adds side by side comparison of expected vs actual results
        hist.add("Expected results: ", [expected_result] * self.num_sides, stroke_style = {"width" : 2})
        hist.render_to_file(filename)
        os.startfile(filename)
    
    def cursor(self, scatter_plot, x, y):
        cursor = mpl.cursor(scatter_plot, hover = True)
        @cursor.connect("add")
        def on_hover(sel):
            sel.annotation.set_text(f"Side: {x[sel.index]} \nFrequency: {y[sel.index]}")

    def visualize_scatter(self, results):
        """Visualizes the rolls of a die in a scatter plot"""
        sides = self.num_sides
        rolls = self.num_rolls
        #range starts from 0 and ends at n - 1 
        x_values = [side for side in range(1, sides + 1)]
        #x value plotted will be the dice numbers, while y value plotted will be dice frequencies
        frequency = self.get_frequencies(results)
        x, y = x_values, frequency
        plt.title(f"Data of rolling a {sides} sided die {rolls} times")
        plt.xlabel("Dice side", fontsize = 14)
        plt.ylabel("Frequency of roll", fontsize = 14)
        scatter_plot = plt.scatter(x, y, label = "Actual Data")
        #calls the cursor method for the plotted points on the scatter plot
        self.cursor(scatter_plot, x, y)

        #expected distribution
        expected_scatter_distribution_y = round(rolls / sides, 2)
        expected_scatter_distribution_x = x_values.copy()
        expected_scatter_distribution_y = [expected_scatter_distribution_y for y in range(1, sides + 1)]
        expected_scatter_distribution = plt.scatter(expected_scatter_distribution_x, expected_scatter_distribution_y, label = "Expected Distribution")
        #calls the cursor method for expected scatter distribution
        self.cursor(expected_scatter_distribution, expected_scatter_distribution_x, expected_scatter_distribution_y)
        plt.legend()
        plt.show()
        self.save_scatter_file()

    def save_scatter_file(self):
        """Automatically give the option to save a scatter file"""
        root = tk.Tk()
        #prevent the blank root from appearing
        root.withdraw()
        save_scatter = messagebox.askyesno("Save", "Save single die scatter plot?")
        #default in case of cancel
        save_path = None
        if save_scatter:
            save_path = filedialog.asksaveasfilename(
                parent = root,
                initialdir = Path.home() / "Desktop",
                initialfile = "single_dice_scatterplot.png",
                title = "Save plot as",
                defaultextension = ".png",
                filetypes = [("PNG Files", "*.png"), ("SVG Files", "*.svg"), ("PDF Files", "*.pdf")]
            )
        else:
            messagebox.showwarning("Notification", "Single dice scatter plot not saved")
        #destroys widget
        root.destroy()
        return save_path