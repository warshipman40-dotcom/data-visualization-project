import pygal
import os
from dice import Die
die_1 = Die()
die_2 = Die()



numOfDiceRolls = int(input("How many times would you like to roll your dice? "))
max_num = die_1.num_sides * die_2.num_sides
results = []
for roll_num in range(numOfDiceRolls):
    result = die_1.roll() * die_2.roll()
    results.append(result)

#analyze data frequency
frequencies = []
percentages = []
for value in range(1, max_num + 1):
    frequency = results.count(value)
    frequencies.append(frequency)
    percentage = round((100 * frequency / len(results)), 2)
    percentages.append(percentage)
    

hist = pygal.Bar()
#uses f-string to format the variable inside the string
hist.title = f"Simulation of rolling a dice {numOfDiceRolls} times"
hist.x_labels = list(range(1, max_num + 1))
hist._x_title = "Possible values"
hist._y_title = "Frequency of result"
hist.add("D6 x D6 (%)", percentages)
hist.render_to_file("D6xD6.svg")
os.startfile("D6xD6.svg")
