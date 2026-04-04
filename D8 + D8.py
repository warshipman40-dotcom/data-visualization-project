import pygal
from dice import Die
die_1 = Die(8)
die_2 = Die(8)

results = []
max_result = die_1.num_sides + die_2.num_sides
for roll_num in range(1000):
    result = die_1.roll() + die_2.roll()
    results.append(result)

frequencies = []
for value in range(2, max_result + 1):
    frequency = results.count(value)
    frequencies.append(frequency)

hist = pygal.Bar()
hist.title = "Results of rolling two 8-sided dice 1000 times"
hist.x_labels = list(range(2, max_result + 1))
hist._x_title = "Result"
hist._y_title = "Frequency of Result"
hist.add("D8 + D8 frequencies", frequencies)
hist.render_to_file("D8 + D8.svg")