import pygal
from dice import Die
#Creates a D6 and D10 die
die_1 = Die()
die_2 = Die(10)

#Makes some rolls and stores the results in the list
results = []
max_result = die_1.num_sides + die_2.num_sides
for roll_num in range(50000):
    #simulates 50,0000 rolls of die_1 + die_2
    result = die_1.roll() + die_2.roll()
    #stores all the rolls in a list to be analyzed later
    results.append(result)

#Analyze the frequencies
frequencies = []
#for values from range 2 to max_result + 1
for value in range(2, max_result+1):
    #checks the frequency of values in rolls 
    frequency = results.count(value)
    frequencies.append(frequency)

#Visualize the results
hist = pygal.Bar()
hist.title = "Results of rolling a D6 and D10 50,000 times"
#generates from 2 to 13 and stores it in labels
hist.x_labels = list(range(2, max_result + 1))
hist.x_title = "Result"
hist.y_title = "Frequency of Result"
hist.add("D6 + D10", frequencies)
hist.render_to_file("D6 + D10.svg")