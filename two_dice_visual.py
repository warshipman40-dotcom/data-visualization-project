import pygal
from dice import Die

#Creates a die_1 object
die_1 = Die()
die_2 = Die()
#Makes some rolls and stores results in list
results = []
for roll in range(1000):
    result = die_1.roll() + die_2.roll()
    results.append(result)

print(results)

#Analyze the results
frequencies = []
max_result = die_1.num_sides + die_2.num_sides
#loops through all possible values
#because range doesn't include the final number
for value in range(2, max_result+1):
    #counts how many times each value occurs
    frequency = results.count(value)
    #appends this value to the list
    frequencies.append(frequency)
print(frequencies)

#Visualize the results using pygal
#creates instance of pygal.Bar
hist = pygal.Bar()
hist.title = "Results of rolling two D6 dice 1000 times"
hist.x_labels = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
hist._x_title = "Result"
hist._y_title = "Frequency of Result"
hist.add("D6 + D6", frequencies)
hist.render_to_file("two_die_visual.svg")