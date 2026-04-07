#main class
import pygal
from dice import Die
from diceroll import DiceGameRoll
import tkinter as tk
from tkinter import messagebox
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
scaled_widget_height = int(screen_height/4)
scaled_widget_width = int(screen_width/4)
screen_middle_width = (screen_width - scaled_widget_width) // 2
screen_middle_height = (screen_height - scaled_widget_height) // 2
#resizes the root to an appropriate size
root.geometry(f"{scaled_widget_width}x{scaled_widget_height}+{screen_middle_width}+{screen_middle_height}")
#creates a frame widget inside of the root window (frame can hold multiple widgets)
frame = tk.Frame(root)
#places the label inside the frame at row 0, column 0 with 5 pixels spacing below and above the label for spacing
#labels is in the east / right of grid cell
tk.Label(frame, text = "Dice One Sides").grid(row = 0, column = 0, pady = 5, sticky = "e")
tk.Label(frame, text = "Dice Two Sides").grid(row = 1, column = 0, pady = 5, sticky = "e")
tk.Label(frame, text = "Number of rolls").grid(row = 2, column = 0, pady = 5, sticky = "e")
#attachs the entry's to the frame
entryOne = tk.Entry(frame)
entryTwo = tk.Entry(frame)
entryThree = tk.Entry(frame)
#entry placed at row 0, column 1, with 5 pixels of vertical padding below and above, and to the west /left of grid cell
entryOne.grid(row = 0 , column = 1, pady = 5, sticky = "w")
entryTwo.grid(row = 1, column = 1, pady = 5, sticky = "w")
entryThree.grid(row = 2, column = 1, pady = 5, sticky = "w")
#this places the frame at 50% of the roots width and 50% of the roots height in the center
frame.place(relx = 0.5, rely = 0.5, anchor = "center")
dice_values = []
def get_values():
    #entry.get() returns a string so it must be converted to int
    global dice_values
    try:
        sideOne = int(entryOne.get())
        sideTwo = int(entryTwo.get())
        numRolls =int(entryThree.get())
        dice_info = [sideOne, sideTwo, numRolls]
        root.destroy()
        return dice_info
    except ValueError:
        #if there is a value error, this uses the built-in entry.delete() function to delete all text in the widget
        #from first character (0) to last character (tk.END)
        entryOne.delete(0, tk.END)
        entryTwo.delete(0, tk.END)
        entryThree.delete(0, tk.END)
        messagebox.showwarning("Value Error", "Please input three integers")
#creates button with the callback fucntion get_values, columnspan of 2 means it is the width of 2 columns
tk.Button(frame, text = "SUBMIT", command = get_values).grid(row = 3, column = 0, columnspan = 2, pady = 10)
root.mainloop()

die_1 = Die(6)
result = die_1.roll_dice(100)
frequencies = die_1.get_frequencies(result)
#we pass result because we calculate frequencies in get_frequencies
#die_1.create_histogram(result)
die_1.visualize_scatter(result)
#more examples
#uses a try except to provide a user friendly message
try: 
    die_2 = Die(dice_values[0])
    die_3 = Die(dice_values[1])
    game = DiceGameRoll([die_2, die_3])
    #dice_values[-1] will always give the last value in the list
    rolls = game.roll_all(dice_values[-1])
except IndexError:
    #informs the user of an index error where the list is not populated
    messagebox.showwarning("Index Error", "Index Error, list is not populated")
    #gives the user the option to use default dice sides or cancel
    #answer can either be the boolean true (Yes) or False (Cancel / No)
    answer = messagebox.askyesnocancel("Option", "Use default dice sides (6) or cancel?")
    if answer:
        die_2, die_3 = Die(), Die()
        game = DiceGameRoll([die_2, die_3])
        rolls = game.roll_all()
    else:
    #cancels if the user chooses to cancel
        messagebox.showinfo("Cancelled", "Dice simulation cancelled")
#uses a try except block to handle exceptions without getting error messages
#in this case this error occurs when the user cancels the dice simulation
try:
    #the two dices are passed in because the parameter requires a list
    products = game.get_product(rolls)
    sums = game.get_sum(rolls)
    possible_products = game.get_all_possible_products()
    possible_sums = game.get_all_possible_sums()
    roll_frequencies = game.get_frequencies(rolls, "sum")
    #game.visualize_histogram_data(rolls)
    #game.visualize_histogram_data(rolls, "dice_products.svg", "product")
    game.visualize_scatter_data(rolls)
    game.visualize_scatter_data(rolls, "product")
    game.compare_scatter_data(rolls)
    key_features = game.get_key_features(rolls)
    game.save_data(rolls)
    game.clear_file_data()
#name error exception is passed so the user doesn't experience too many error messages
except NameError:
    pass
    #messagebox.showwarning("Error", "Name not defined")