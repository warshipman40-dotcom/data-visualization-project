from dice import Die
from collections import Counter
from sklearn.metrics import r2_score
import pygal
import json
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from pathlib import Path
import mplcursors as mpl
import os
class DiceGameRoll:
    """A class that allows you to roll multiple dice and find product / sum"""
    def __init__(self, dice):
        #stores a list of dice
        self.dice = dice
        
    #this method of DiceGameRoll will pass in a list of die
    #if let blank, will roll 100 times by default  
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

    def get_key_features(self, results, type = "sum", percentile = 25):
        """Finds key features of a dataset (default values set type = sum, percentile = 25)"""
        #this creates a dictionary where the name of the key feature and the value of the key feature can be stored
        key_features = {}
        #this variable stores the list of sums from results
        total_sum = self.get_sum(results)
        #this variable stores the list of products from results
        total_products = self.get_product(results)
        #uses a dictionary to store values
        if type == "sum":
            #this will find the average of the total sums list
            key_features["mean"] = np.mean(total_sum)
            #this will find the median of the total sums list
            key_features["median"] = np.median(total_sum)
            #counter method will essentially build a {value : frequency} dictionary for you
            #example of counter -> counter = {4 : 3, 5 : 2, 1 : 3}
            counter = Counter(total_sum)
            #max_freq will store the frequency of the most common value
            max_freq = max(counter.values())
            #since counter is basically a dictionary, .items() turns it into a tuple (key, value)
            #for val, freq unpacks the tuple, stores key -> value, value -> freq
            #freq == max_freq acts a filter ; it only keeps the values whose frequency is equal to the max frequency
            #the first val will determine what goes in the list modes while the second one is part of (val, freq) in the tuple unpacking
            modes = [val for val, freq in counter.items() if freq == max_freq]
            #mode is the most frequent outcome
            key_features["mode"] = {
                "value" : modes,
                "frequency" : max_freq
            }
            #standard deviance describes how close the values are to the mean
            key_features["standard_deviation"] = round(np.std(total_sum), 3)
            #standard deviance is the square root of variance
            key_features["variance"] = round(np.var(total_sum), 3)
            key_features["percentile"] = np.percentile(total_sum, percentile)
        
        elif type == "product":
            #key_features["max"] = max(total_products)
            #key_features["min"] = min(total_products)
            key_features["mean"] = np.mean(total_products)
            key_features["median"] = np.median(total_products)
            counter = Counter(total_products)
            max_freq = max(counter.values())
            modes = [val for val, freq in counter.items() if freq == max_freq]
            key_features["mode"] = {
                "value" : modes,
                "frequency" : max_freq
            }
            key_features["standard_deviation"] = round(np.std(total_products), 3)
            key_features["variance"] = round(np.var(total_products), 3)
            key_features["percentile"] = np.percentile(total_products, percentile)
        print(f"Returning key features of total {type.title()}'s")
        return key_features
    
    def visualize_histogram_data(self, results, filename = r"C:\Users\warsh\Downloads\python_work\Data Visualization\sumOfDice.svg", type = "sum", ):
        """Visualizes either the sum or product in a histogram"""
        #list comprehension
        #for each die in the list of dice, the number of sides is stored as a string in sides
        sides = [str(die.num_sides) for die in self.dice]
        #these sides are then joined and stored in sides_text
        self.sides_text = ", ".join(sides)
        hist = pygal.Bar()
        #uses f-strings so that variables can be inserted into the title
        hist.title = f"{type.title()} of rolling {self.total_rolls} times! ({self.sides_text} sided dice)"
        hist.x_title = "Results"
        hist.y_title = "Frequencies"
        #we use an if / else to determine if we are labelling with products or sum
        if type == "product":
            hist.x_labels = self.get_all_possible_products()
            hist.add("Data", self.get_frequencies(results, "product"))
        elif type == "sum":
            hist.x_labels = self.get_all_possible_sums()
            hist.add("Data", self.get_frequencies(results))
        #this stores the histogram on a file
        hist.render_to_file(filename)
        #this uses os module to automatically open this file
        os.startfile(filename)

    #default percentile
    def visualize_scatter_data(self, results, type = "sum", percentile = 25):
        """Visualizes either the sum or product in a scatter plot"""
        sides = [str(die.num_sides) for die in self.dice]
        #the self in self.sides_text allows it to be stored in memory and used in different methods
        self.sides_text = ", ".join(sides)
        sum_frequencies = self.get_frequencies(results)
        product_frequencies = self.get_frequencies(results, "product")
        plt.title(f"Frequency Analysis of rolling {self.total_rolls} times! ({self.sides_text} sided dice)")
        plt.ylabel(f"Frequency of {type.title()}", fontsize = 18)
        #step basically divides the ticks into 10 sections and ensures it is > 1
        step = max(1, max(sum_frequencies) // 10)
        #plt.yticks put ticks from 0 all the way to the maximum value in frequency, moving up by the value of step each time
        plt.yticks(range(0, max(sum_frequencies) + 1, step))
        
        if type == "product":
            x, y = self.get_all_possible_products(), product_frequencies
            plt.xlabel("Product", fontsize = 14)
            scatter = plt.scatter(x, y)

            key_product_features = self.get_key_features(results, "product", percentile = 25)
            mode_value = key_product_features["mode"]["value"]
            mode_freq = key_product_features["mode"]["frequency"]
            #stores the value in a variable
            plt.scatter(mode_value, mode_freq, color="red")
            #median_value represents the x_value of the median
            median_value = key_product_features["median"]
            percentile_value = key_product_features["percentile"]
            mean_value = key_product_features["mean"]
            #plots green dotted line at median_value
            plt.axvline(x = median_value, color = "green", linestyle = "--", label = f"Median of dice products = {median_value}")
            #plots black dotted line at mean value
            plt.axvline(x = mean_value, color = "black", linestyle = "--", label = f"Mean of dice products = {mean_value}")
            #plots yellow line at percentile value (user input for percentile)
            plt.axvline(x = percentile_value, color = "yellow", linestyle = "--", label = f"{percentile}th percentile of dice products = {percentile_value}")
            plt.legend()
            #creates a polynomial model
            my_model = np.poly1d(np.polyfit(x, y, 3))
            #specifys where the line will display (where we start, where we end, and the highest point)
            myline = np.linspace(min(x), max(x), max(y))
            plt.plot(myline, my_model(myline))
            relationship = round(r2_score(y, my_model(x)), 3)

        elif type == "sum":
            x, y = self.get_all_possible_sums(), sum_frequencies
            plt.xlabel("Sum", fontsize = 14)
            #creates a scatter plot of our graph
            scatter = plt.scatter(x, y)
            #gets the key features dictionaries and stores them in these variables
            key_sum_features = self.get_key_features(results)
            #extracts mode value (sum that was rolled most frequently and stores into this variable)
            mode_value = key_sum_features["mode"]["value"]
            #extracts mode frequency (the number of times the mode value was rolled and stores into this variable)
            mode_freq = key_sum_features["mode"]["frequency"]
            #using the mode value (x-value) and mode_freq (y-value) plots in the color red
            #mode_value is a list that contains values inside of it (to plot multiple modes)
            for val in mode_value:
                plt.scatter(val, mode_freq, color="red")
            median_value = key_sum_features["median"]
            percentile_value = key_sum_features["percentile"]
            mean_value = key_sum_features["mean"]
            #this plots a green dotted line at the median value
            plt.axvline(x = median_value, color = "green", linestyle = "--", label = f"Median of dice sums = {median_value}")
            plt.axvline(x = mean_value, color = "black", linestyle = "--", label = f"Mean of dice sums = {mean_value}")
            plt.axvline(x = percentile_value, color = "yellow", linestyle = "--", label = f"{percentile}th percentile of dice sums = {percentile_value}")
            plt.legend()
            #passes in our x and y values and creates a 3rd degree polynomial
            my_model = np.poly1d(np.polyfit(x, y, 3))
            myline = np.linspace(min(x), max(x), max(y))
            plt.plot(myline, my_model(myline))
            #a relationship of 1 means a very good fit / 0.0 means the mean / less than 0.0 is a very bad fit
            #r2_score is a method we import
            #we pass in actual data (y) and model predictions (my_model(x)) to calculate the r2 score
            relationship = round(r2_score(y, my_model(x)), 3)
       
        #{:.2f} will format to two decimal places
        #the 0.1 means 7.5% from the left and the 0.9 means 90% from the bottom
        #transform = plt.gca().transAxes basically tells python to use the transAxes system regardless of data limits(meaning it doesn't change)
        #otherwise our text would shift based on the range of the axes, making it inconsistent
        #plt.text(0.075, 0.9, "y = "  + "{:.2f}".format(slope) + "x" + " + {:.2f}".format(intercept), size = 12, transform=plt.gca().transAxes)
        plt.text(0.6, 0.8, f"Relationship = {relationship} \n0 = NR \n|1| = 100% R", size = 12, transform = plt.gca().transAxes)
        plt.tick_params(axis = "both", labelsize = 14)
        #uses the mplcursors library
        cursor = mpl.cursor(scatter, hover = True)
        #basically the event is add, so each time you hover over a point, mpl_cursors adds a tooltip
        #the @ symbol is a decorator, which connects the cursor connect event with on_hover function
        @cursor.connect("add")
        #sel is basically is an object that represents the point you are currently hovering over
        def on_hover(sel):
            if type == "sum":
                #we store the lists into variables just to make it less time consuming
                sums = self.get_all_possible_sums()
                frequencies = sum_frequencies
                #creates an annotation to display the x/y values
                #We use type.title() because the text will be variable based on whether we want product / sum
                #Frequency is a constant so we don't use a variable
                #Sel.index basically helps you get the actual values at the position of the sel object
                sel.annotation.set_text(f"{type.title()}: {sums[sel.index]} \nFrequency: {frequencies[sel.index]}")

            elif type == "product":
                products = self.get_all_possible_products()
                frequencies = product_frequencies
                sel.annotation.set_text(f"{type.title()}: {products[sel.index]} \nFrequency: {frequencies[sel.index]}")
        plt.grid(color = "grey", linestyle = "--", linewidth = 0.5)
        plt.show()
        self.choose_scatter_save_file()

    def choose_scatter_save_file(self):
        """Automatically gives the option to save scatter plots to a file"""
        root = tk.Tk()
        #prevents the blank root from showing
        root.withdraw()
        save_scatter = messagebox.askyesno("Save", "Save scatter plot?")
        #automtically opens the save as dialog from your operating system
        #default in case the user doesn't save
        save_path = None
        if save_scatter:
            save_path = filedialog.asksaveasfilename(
                parent = root,
                #default folder
                initialdir = Path.home() / "Desktop",
                #default file name
                initialfile = "scatter_plot.png",
                title = "Save plot as",
                #default filetype png
                defaultextension = ".png",
                #defines the valid filetypes
                filetypes = [("PNG Files", "*.png" ), ("SVG Files", "*.svg"), ("PDF Files", "*.pdf")]
            )
            messagebox.showinfo("Notification", "Scatter plot successfully saved!")
        else:
            messagebox.showwarning("Notifcation", "Scatter plot not saved")
        #destroys the widget (root)
        root.destroy()
        return save_path
    
    def compare_scatter_data(self, results):
        plt.suptitle(f"Product vs Sum of rolling {self.sides_text} sided die {self.total_rolls} times!")
        #we need to get the lists of all possible products / sums and frequencies
        #np.array() basically converts these lists to numPy arrays, allowing us to do lienar algebra and graph a line of best fit
        products = np.array(self.get_all_possible_products())
        sums = np.array(self.get_all_possible_sums())
        product_frequencies = np.array(self.get_frequencies(results, "product"))
        sum_frequencies = np.array(self.get_frequencies(results))
        #this plot has 1 row, 2 columns, and this subplot is the first plot
        plt.subplot(1, 2, 1)
        plt.title("Sums")
        #returns a scatter object which contains all plotted points and positions
        scatter_sum = plt.scatter(sums, sum_frequencies)
        #checks for mouse interactions (tooltips appear when you hover)
        cursor_sum = mpl.cursor(scatter_sum, hover = True)
        #@ is decorater (connects function with event)
        #When a new annotation (tooltip) is shown, the function is run
        @cursor_sum.connect("add")
        #sel is an object created by mpl.cursor that basically represents the point we currently hover over
        #sel is a container of information including index
        #sel.index is basically a point (x, y)
        def on_hover_sum(sel):
            sel.annotation.set_text(f"Sum: {sums[sel.index]} \nFrequency: {sum_frequencies[sel.index]}")

        #this plot has 1 row, 2 columns, and this subplot is the second plot
        plt.subplot(1, 2, 2)
        plt.title("Products")
        scatter_product = plt.scatter(products, product_frequencies, c="red")
        cursor_product = mpl.cursor(scatter_product, hover = True)
        @cursor_product.connect("add")
        def on_hover_product(sel):
            sel.annotation.set_text(f"Product: {products[sel.index]} \nFrequency : {product_frequencies[sel.index]}")
        plt.show()  
        #default name dice_results.json, default type = sum
    
    def save_data(self, results, filename = "dice_results.json", type = "sum"):
        """Save dice results and key features into a JSON file"""
        #checks if the type will be a sum/product
        if type == "sum":
            values = self.get_all_possible_sums()
            frequencies = self.get_frequencies(results)
            key_features = self.get_key_features(results)
        elif type == "product":
            values = self.get_all_possible_products()
            frequencies = self.get_frequencies(results, "product")
            key_features = self.get_key_features(results, "product")
        #stores the data into a dictionary 
        data = {
            "values" : values, 
            "frequencies" : frequencies, 
            "key_features" : key_features
        }
        #makes sure that the file exists
        if os.path.exists(filename):
            #opens and reads the file
            #using write will overwrite, which is why we use read
            #this method will basically store our existing data from the file using json.load()
            #and store it existing data, before appending our new data (data) to essentially append our data at the end
            with open(filename, "r") as file:
                try:
                    #converts the json data into a python object like a dictionary
                    existing_data = json.load(file)
                #make sure it's a list so we can use append
                    if not isinstance(existing_data, list):
                        #if not a list, turns it into a list
                        existing_data = [existing_data]
                except json.JSONDecodeError:
                    #if an error is encountered, start with an empty file
                    existing_data = []
        else:
            #if file doesn't exist, start withs an empty file
            existing_data = []
        #directly appending doesn't work with JSON because it breaks the structure
        existing_data.append(data)
        with open(filename, "w") as file:
                #this converts a python object into a json string
                #indenting makes easier to read results
                #json.dump must dump existing data to a JSON file because existing data contains all of our new data
                #this is because our data gets wiped each time when we use write
                json.dump(existing_data, file, indent = 3)
        print(f"Data succesfully saved to {filename}!")

    def clear_file_data(self, filename = "dice_results.json", confirmation = True):
        """Clears all data from the file"""
        #function gets called when the cancel button is clicked
        def cancel_action():
            messagebox.showinfo("Operation Cancelled", "File deletion cancelled", parent = root)
            root.destroy()
        #function is called when confirmation button is clicked
        def prompt_user():
             #creates a messagebox
             #parent = root ensures that messagebox always appears on top of root
            confirmation = messagebox.askyesnocancel("Confirmation", f"Delete {filename}?", parent = root)
            #confirmation_label.pack()
            #confirmation_entry.pack()
            #confirmation_entry.focus()
            if confirmation:
            #asks a second confirmation to make 100% sure the user wants to wipe their data
                second_confirmation = messagebox.askyesno("Confirm Again", "Confirm Again", parent = root)
                #message.box() returns a boolean 
                if second_confirmation:
                #since writing to a file automatically clears the file, we use pass to just clear the file without writing
                    with open(filename, "w") as file:
                        pass
                    messagebox.showinfo("Success", "File Succesfully Cleared!")
                    os.startfile(filename)
                    root.destroy()
        
        #creates the widget object and stores in root
        #uses toplevel because in the main theres already a tk.Tk()
        #toplevel is linked to the existing root in the main class
        root = tk.Tk()
        #registers a callback function on root event ("WM_DELETE_WINDOW")
        #callback function on_close
        def on_close():
            messagebox.showinfo("Success", "Succesfully saved data!")
            #closes root after succesfully showing message
            root.destroy()
        #protocol runs 
        root.protocol("WM_DELETE_WINDOW", on_close)
        #this then forces the window to stay above all other windows on computer
        root.attributes("-topmost", True)
        #this gives the window time to go to the top, and then resets after
        root.after(0, lambda: root.attributes("-topmost", False))
        #var = tk.StringVar(value = "yes")
        #confirmation_entry = ttk.Entry(root, textvariable = var, width=50, font=("Arial", 12))
        #confirmation_label = ttk.Label(root, text = f"Clear Data \n(Yes / No)")
        #these functions get the width and height of a device screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        scaled_widget_width = int(screen_width / 4)
        scaled_widget_height = int(screen_height / 4)
        screen_middle_width = int(screen_width / 2)
        screen_middle_height = int(screen_height / 2)

        screen_middle_width = (screen_width - scaled_widget_width) // 2
        screen_middle_height = (screen_height - scaled_widget_height) // 2

        #order of width * height
        root.geometry(f"{scaled_widget_width}x{scaled_widget_height}+{screen_middle_width}+{screen_middle_height}")
        tk.Label(root, text = f"Clear {filename}?", font = ("Arial", 20)).pack()
        #creates the confirm button object
        confirm = tk.Button(root, text = "CONFIRM", width = 12, command = prompt_user)
        #packs the confirm button in a window / widget
        confirm.pack(side = "left", padx = 40)
        #root.destroy() immediately closes the window
        cancel = tk.Button(root, text = "CANCEL", width = 12, command = cancel_action)
        cancel.pack(side = "right", padx = 40)
        #starts an infinite loop for the window/widget object (root) and waits for an event
        root.mainloop()

            

