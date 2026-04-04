import pygal
from dice import Die
from diceroll import DiceGameRoll
side = int(input("How many sides do you want your first dice to have? "))
side_two = int(input("How many sides do you want your second dice to have? "))
die_1 = Die()
result = die_1.roll_dice(1000)
frequencies = die_1.get_frequencies(result)
#we pass result because we calculate frequencies in get_frequencies
die_1.create_histogram(result)

#more examples 
die_2 = Die(side)
die_3 = Die(side_two)
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
print("Possible sums: \n" + str(possible_sums))

roll_frequencies = game.get_frequencies(rolls, "sum")

game.visualize_histogram_data(rolls)
game.visualize_histogram_data(rolls, "dice_products.svg", "product")
game.visualize_scatter_data(rolls)
game.visualize_scatter_data(rolls, "product")