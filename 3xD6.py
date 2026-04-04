import pygal
from dice import Die
die_1 = Die()
die_2 = Die()
die_3 = Die()

max_result = die_1.num_sides + die_2.num_sides + die_3.num_sides
results = []
for roll_num in range(1000):
    roll_num = die_1.roll() + die_2.roll() + die_3.roll()
    results.append(roll_num)

frequencies = []
percentages = []
#this is every value from the mininum to  max 
#+1 is used because range scope is to n-1
for value in range(3, max_result + 1):
    #this gives the total number of values that match with the current iteration of value
    frequency = results.count(value)
    #this adds the total number of occurences to our new list
    frequencies.append(frequency)
    percentage = frequency / len(results)
    percentages.append(percentage)

hist = pygal.Bar()
hist.title = "Results of rolling 3 D6 dice 1000 times"
hist.x_labels = list(range(3, max_result + 1))
hist._x_title = "Results"
hist._y_title = "Frequencies"
#this ensures the bar has the height of the value in frequencies for each
hist.add("D6 x 3", percentages)
hist.render_to_file("D6 x 3.svg")