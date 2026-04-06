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
screen_middle_width = int(screen_width / 2)
screen_middle_height = int(screen_height / 2)
screen_middle_width = (screen_width - scaled_widget_width) // 2
screen_middle_height = (screen_height - scaled_widget_height) // 2
#resizes the root to an appropriate size
root.geometry(f"{scaled_widget_width}x{scaled_widget_height}+{screen_middle_width}+{screen_middle_height}")


tk.Label(root, text = "Dice One Sides").grid(row = 0)
tk.Label(root, text = "Dice Two Sides").grid(row = 1)
entryOne = tk.Entry(root)
entryTwo = tk.Entry(root)
entryOne.grid(row = 0 , column = 1)
entryTwo.grid(row = 1, column = 1)
dice_values = []
def get_values():
    #entry.get() returns a string so it must be converted to int
    global dice_values
    try:
        sideOne = int(entryOne.get())
        sideTwo = int(entryTwo.get())
        dice_values = [sideOne, sideTwo]
        root.destroy()
        return dice_values
    except ValueError:
        messagebox.showwarning("Value Error", "Please input two integers")

tk.Button(root, text = "SUBMIT", command = get_values).grid(row = 2, column = 0, columnspan = 2)
root.mainloop()

die_1 = Die(6)
result = die_1.roll_dice(100)
frequencies = die_1.get_frequencies(result)
#we pass result because we calculate frequencies in get_frequencies
die_1.create_histogram(result)
die_1.visualize_scatter(result)
#more examples 
die_2 = Die(dice_values[0])
die_3 = Die(dice_values[1])
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