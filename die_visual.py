import pygal
from dice import Die

#Creates a die object
die = Die()

#Makes some rolls and stores results in list
results = []
for roll in range(1000):
    result = die.roll()
    results.append(result)

print(results)

#Analyze the results
frequencies = []
#loops through all possible values
for value in range(1, die.num_sides + 1):
    #counts how many times each value occurs
    frequency = results.count(value)
    #appends this value to the list
    frequencies.append(frequency)
print(frequencies)

#Visualize the results using pygal
#creates instance of pygal.Bar()
hist = pygal.Bar()
hist.title = "Results of rolling 1000 times"
hist.x_labels = ["1", "2", "3", "4", "5", "6"]
hist._x_title = "Result"
hist._y_title = "Frequency of Result"
hist.add("D6", frequencies)
hist.render_to_file("die_visual.svg")