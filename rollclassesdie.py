import pygal
from dice import Die
from diceroll import DiceGameRoll
from tkinter import Entry
import tkinter as tk
from tkinter import ttk

#create an entry object, and a root window
mw = tk.Tk()
mw.title("Dice sides input")
diceOneLabel = ttk.Label(mw, text = "Dice One Sides:")
diceOneLabel.pack(pady = 2)
diceOneSides = ttk.Entry(mw)

diceTwoLabel = ttk.Label(mw, text = "Dice Two Sides:")
diceTwoLabel.pack(pady = 2)
diceTwoSides = ttk.Entry(mw)
#mw.withdraw()
#mw.update_idletasks()
screen_width = mw.winfo_screenwidth()
screen_height = mw.winfo_screenheight()
scaled_widget_height = int(screen_height / 4)
scaled_widget_width = int(screen_width / 4)
middle_screen_width = int(screen_width / 2)
middle_screen_height = int(screen_height / 2)

x = (screen_width- scaled_widget_width) // 2
y = (screen_height - scaled_widget_height) // 2
mw.geometry(f"{scaled_widget_width}x{scaled_widget_height}+{x}+{y}")
mw.deiconify()
mw.lift()
mw.mainloop()


#side = int(input("How many sides do you want your first dice to have? "))
#side_two = int(input("How many sides do you want your second dice to have? "))
die_1 = Die(5)
result = die_1.roll_dice(45)
frequencies = die_1.get_frequencies(result)
#we pass result because we calculate frequencies in get_frequencies
die_1.create_histogram(result)

#more examples 
die_2 = Die(6)
die_3 = Die(6)
#the two dices are passed in because the parameter requires a list
game = DiceGameRoll([die_2, die_3])
rolls = game.roll_all(50)
products = game.get_product(rolls)
#print("Products:\n" + str(products))

sums = game.get_sum(rolls)
#print("Sums: \n" + str(sums))

possible_products = game.get_all_possible_products()
#print("Possible products: \n" + str(possible_products))

possible_sums = game.get_all_possible_sums()
#print("Possible sums: \n" + str(possible_sums))
roll_frequencies = game.get_frequencies(rolls, "sum")
game.visualize_histogram_data(rolls)
game.visualize_histogram_data(rolls, "dice_products.svg", "product")
game.visualize_scatter_data(rolls)
game.visualize_scatter_data(rolls, "product")
game.compare_scatter_data(rolls)
key_features = game.get_key_features(rolls)
#print(game.get_sum(rolls))
#print("Mode : " + str(key_features["mode"]))
#print("Standard Deviation: " + str(key_features["standard_deviation"]))
game.save_data(rolls)
game.clear_file_data()