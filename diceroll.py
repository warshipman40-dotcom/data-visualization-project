from dice import Die
import pygal
import matplotlib.pyplot as plt
import mplcursors as mpl
import os
class DiceGameRoll:
    """A class that allows you to roll multiple dice and find product / sum"""
    def __init__(self, dice):
        #stores a list of dice
        self.dice = dice
        
    #this method of DiceGameRoll will pass in a list of die 
    def roll_all(self, total_rolls = 100):
        self.total_rolls = total_rolls
        """This lets you combine dice with different sides"""
        #this will let you combine dice with different sides and examine data
        results = []
        for roll in range(total_rolls):
            value = [die.roll() for die in self.dice]
            results.append(value)
        return results
    
    def get_product(self, results):
        """Function allows you to get a list full of dice products"""
        products = []
        #because products will be like [[5, 2], [3,4], [2, 6]]
        #we have to use two for loops to get the item i nthe list, and the values of the items inside
        for item in results:
            product = 1
            for value in item:
                product *= value
            #this will append the value to products list
            products.append(product)    
        return products
    
    def get_sum(self, results):
        """This function allows you to get a list of dice sums"""
        sums = []
        for item in results:
            itemSum = sum(item)
            sums.append(itemSum)
        return sums
    #to get all possible products, we need to get the number of sides from both dice
    #then we have to make a nested for loop so that every possibiltiy is multiplied
    #after that, we have to remove duplicates so the results aren't skewed
    def get_all_possible_products(self):
        """This function allows you to get a list of all possible products given the dice values"""
        possible_products = [1]
        #loops through all die in the list self.dice
        for die in self.dice:
            #we have to use this to prevent a memory leak so that the list doesn't keep growing at an exponential rate
            current_products = possible_products.copy()
            #this will loop over the current products, not the ones we just appended
            for product in current_products:
                #this stores the possible range from 1 to total die sides in the variable value
                for value in range (1, die.num_sides+1):
                    #this will than append to list and keep getting multiplied
                    possible_products.append(product * value)
        #using set will remove duplicates (since set can't contain duplicates, the duplicates will automatically get removed)
        possible_products = sorted(set(possible_products))
        return possible_products

    def get_all_possible_sums(self):
        """This function allows you to get a list of all possible sums given the dice sums"""
        #to get all possible sums, we need to add all possible values between the two pairs of dice
        #to get all possible values we must use nested for loops
        #we must start with 0 so the list is actually iterable
        possible_sums = [0]
        for die in self.dice:
            #we use a copy of the list 
            #current_sums contains all information in possible_sums at the specific moment
            #it does NOT change when you iterate over it
            #this helps you safely iterate over both lists and get the possible sum
            current_sums = possible_sums.copy()
            #this will erase the old list, getting rid of 0 being one of our possible sums
            possible_sums = []
            #values is all the possible values we can get from the sides of both dice so far
            #we use this loop in the range of current_sums because we need to loop 
            for sum in current_sums:
                for values in range(1, die.num_sides+1):
                    possible_sums.append(values + sum)
            
        possible_sums = sorted(set(possible_sums))
        return possible_sums

    def get_frequencies(self, results, type = "sum"):
        """Return the frequencies of value occurences"""
        frequencies = []
        #checks if we are looking for a sum or a product
        if type == "sum":
            possible_values = self.get_all_possible_sums()
            #this checks values from 1 to the max of the sums list
            for value in possible_values:
                #checks the list we get from self.get_all_possible_sums() and uses count() to see 
                #how many iterations of value match with each possible sum inside the list
                frequencyOfValue = self.get_sum(results).count(value)
                #appends the value of total matches in our frequencies list
                frequencies.append(frequencyOfValue)
        elif type == "product":
            possible_values = self.get_all_possible_products()
            for value in possible_values:
                frequencyOfValue = self.get_product(results).count(value)
                frequencies.append(frequencyOfValue)
        #returns frequencies so we can use it 
        return frequencies

    #def get_key_features(self, results, type = "sum"):
        #key_features = {}
        #if type == "sum":
            #average = 
        #elif type == "product":


    def visualize_histogram_data(self, results, filename = r"C:\Users\warsh\Downloads\python_work\Data Visualization\sumOfDice.svg", type = "sum", ):
        """Visualizes either the sum or product in a histogram"""
        #list comprehension
        #for each die in the list of dice, the number of sides is stored as a string in sides
        sides = [str(die.num_sides) for die in self.dice]
        #these sides are then joined and stored in sides_text
        sides_text = ", ".join(sides)
        hist = pygal.Bar()
        #uses f-strings so that variables can be inserted into the title
        hist.title = f"{type.title()} of rolling {self.total_rolls} times! ({sides_text} sided dice)"
        hist.x_title = "Results"
        hist.y_title = "Frequencies"
        #we use an if / else to determine if we are labelling with products or sum
        if type == "product":
            hist.x_labels = self.get_all_possible_products()
            hist.add("Data", self.get_frequencies(results, "product"))
        elif type == "sum":
            hist.x_labels = self.get_all_possible_sums()
            hist.add("Data", self.get_frequencies(results))
        #this stores the histogram o na fire
        hist.render_to_file(filename)
        #this uses os module to automatically open this file
        os.startfile(filename)

    def visualize_scatter_data(self, results, type = "sum"):
        """Visualizes either the sum or product in a scatter plot"""
        sides = [str(die.num_sides) for die in self.dice]
        sides_text = ", ".join(sides)
        plt.title(f"Frequency Analysis of rolling {self.total_rolls} times! ({sides_text} sided dice)")
        plt.ylabel(f"Frequency of {type.title()}", fontsize = 24)
        #step basically divides the ticks into 10 sections and ensures it is > 1
        step = max(1, max(self.get_frequencies(results)) // 10)
        #plt.yticks put ticks from 0 all the way to the maximum value in frequency, moving up by the value of step each time
        plt.yticks(range(0, max(self.get_frequencies(results)) + 1, step))
        if type == "product":
            plt.xlabel("Product", fontsize = 14)
            #plt.scatter(self.get_all_possible_products(), self.get_frequencies(results, "product"))
            scatter = plt.scatter(self.get_all_possible_products(), self.get_frequencies(results, "product"))
       
        elif type == "sum":
            plt.xlabel("Sum", fontsize = 14)
            #plt.scatter(self.get_all_possible_sums(), self.get_frequencies(results))
            scatter = plt.scatter(self.get_all_possible_sums(), self.get_frequencies(results))
        plt.tick_params(axis = "both", labelsize = 14)

        #uses the mplcursors library 
        cursor = mpl.cursor(scatter, hover = True)
        #basically the event is add, so each time you hover over a point, mpl_cursors adds a tooltip
        #the @ symbol is a decorator, which connects the cursor connect event with on_hover function
        @cursor.connect("add")
        def on_hover(sel):
            if type == "sum":
                #we store the lists into variables just to make it less time consuming
                sums = self.get_all_possible_sums()
                frequencies = self.get_frequencies(results)
                #creates an annotation to display the x/y values
                sel.annotation.set_text(f"{type.title()}: {sums[sel.index]} \nFrequency: {frequencies[sel.index]}")
            elif type == "product":
                products = self.get_all_possible_products()
                frequencies = self.get_frequencies(results, "product")
                sel.annotation.set_text(f"{type.title()}: {products[sel.index]} \nFrequency: {frequencies[sel.index]}")
        plt.show()