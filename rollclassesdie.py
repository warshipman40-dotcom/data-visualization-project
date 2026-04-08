#main class
import pygal
from dice import Die
from diceroll import DiceGameRoll
import tkinter as tk
from tkinter import messagebox
from PIL import Image
import json
import sys
#this takes in the parameters of file, and lasts for the paramater duration
def show_gif_then_input(file, duration = 3000):
    #animation method inside of the class
    def animation(current_frame = 0):
        #stores the current frame of photo_image_objects in the variable image
        image = photoimage_objects[current_frame]
        #updates the gif_label to show the current frame
        gif_label.configure(image = image)
        #+1 moves to next frame, restarts at frame 0 when it reaches the end
        current_frame = (current_frame + 1) % frames
        #this waits 50 ms, and calls animation(current_frame) again
        splash.after(50, animation, current_frame)
    #using PIL, opens the GIF and counts how many frames there are
    info = Image.open(file)
    frames = info.n_frames
    photoimage_objects = []
    for image in range(frames):
        #this loops through each frame object and stores it into photoImage
        #this photoImage is stored into a list
        img = tk.PhotoImage(file = file, format = f"gif -index {image}")
        photoimage_objects.append(img)
    #creates a splash window (seperate from root and uses TopLevel())
    splash = tk.Toplevel()
    #this will remove the title bar and close / minimize screens so it looks like a proper splash screen
    splash.overrideredirect(True)
    #this gets the heights and width of a photoimage_object (they all have the same width / height so using [0] works)
    splash_width, splash_height = photoimage_objects[0].width(), photoimage_objects[0].height()
    screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
    splash_middle_width = (screen_width - splash_width) // 2
    splash_middle_height = (screen_height - splash_height) // 2
    #this centers the window using splash.geometry
    splash.geometry(f"{splash_width}x{splash_height}+{splash_middle_width}+{splash_middle_height}")
    #this is the label where the splash screen is displayed
    gif_label = tk.Label(splash, image ="")
    gif_label.pack()
    #calls animation function and starts the animation
    messagebox.showinfo("Running", "Welcome to Data Visualization!")
    animation()
    #after (duration) ms, the splash screen automatically destroys itself
    splash.after(duration, splash.destroy)
    #return splash


#plan for later (add graphics?)
#e.g dice rolling graph, start screen graphic etc
root = tk.Tk()
root.title("Menu")
#this will initially hide the root so the splash can display
root.withdraw()
file = "dice_gif.gif"
#this calls the splash function for 3 seconds and passes in the gif file
splash = show_gif_then_input(file, duration = 3000)
#after 3000 seconds, uses an anonymous lambda function to call root.deiconify(), which shows the main root again
root.after(3000, lambda : root.deiconify())
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
scaled_widget_height = int(screen_height/4)
scaled_widget_width = int(screen_width/4)
screen_middle_width = (screen_width - scaled_widget_width) // 2
screen_middle_height = (screen_height - scaled_widget_height) // 2
#resizes the root to an appropriate size
root.geometry(f"{scaled_widget_width}x{scaled_widget_height}+{screen_middle_width}+{screen_middle_height}")
#creates a frame widget inside of the root window (frame can hold multiple widgets)
frame = tk.Frame(root)
#these will all expand at the same rate
frame.grid_columnconfigure(0, weight = 1)
frame.grid_columnconfigure(1, weight = 1)
frame.grid_columnconfigure(2, weight = 1)
#places the label inside the frame at row 0, column 0 with 5 pixels spacing below and above the label for spacing
#labels is in the east / right of grid cell
#columnspan = 3 means the title spans across all 3 columns, pady = 5 means 5 pixels of vertical spacing
tk.Label(frame, text = "Data Visualization", font = ("Arial", 14)).grid(row = 0, column = 0, columnspan = 3, pady = 5)
#sticky = "e" align the text to the east
tk.Label(frame, text = "Dice One Sides").grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "e")
tk.Label(frame, text = "Dice Two Sides").grid(row = 2, column = 0, padx = 5, pady = 5, sticky = "e")
tk.Label(frame, text = "Number of rolls").grid(row = 3, column = 0, padx = 5, pady = 5, sticky = "e")
#attachs the entry's to the frame
entryOne = tk.Entry(frame)
entryTwo = tk.Entry(frame)
entryThree = tk.Entry(frame)
#entry placed at row 0, column 1, with 5 pixels of vertical padding below and above, and to the west /left of grid cell
#columnspan = 2 makes it span across column 1 and 2 so it is wider
entryOne.grid(row = 1 , column = 1, pady = 5, columnspan = 2,  sticky = "w")
entryTwo.grid(row = 2, column = 1, pady = 5, columnspan = 2, sticky = "w")
entryThree.grid(row = 3, column = 1, pady = 5, columnspan = 2, sticky = "w")
#this places the frame at 50% of the roots width and 50% of the roots height in the center
frame.place(relx = 0.5, rely = 0.5, anchor = "center")
#focuses on entryOne so you can type into it
entryOne.focus()
dice_info = []

def get_values():
    #entry.get() returns a string so it must be converted to int
    global dice_info
    try:
        sideOne = int(entryOne.get())
        sideTwo = int(entryTwo.get())
        numRolls = int(entryThree.get())
        dice_info = [sideOne, sideTwo, numRolls]
        root.destroy()
        return dice_info
    except ValueError:
        #if there is a value error, this uses the built-in entry.delete() function to delete all text in the widget
        #from first character (0) to last character (tk.END)
        entryOne.delete(0, tk.END)
        entryTwo.delete(0, tk.END)
        entryThree.delete(0, tk.END)
        messagebox.showwarning("Value Error", "Please input three integers")

#for get feedback the button has to lead to a seperate entry on a seperate frame
#current frame can be hidden using root.withdraw() and shown again using root.deiconify()
#JSON.dump should be used to store the responses in a file, or whatever is most suitable for storing text
#confirmation message should be sent usings messagebox that the response was recieved and will be reviewed in time

def get_feedback():
    #hides the root
    root.withdraw()
    #creates a Toplevel widget
    feedback_window = tk.Toplevel()
    #titles the window "Feedback"
    feedback_window.title("Feedback")
    #this changes the size and window of the feedback widget using the geometry method
    feedback_window.geometry(f"{scaled_widget_width}x{scaled_widget_height}+{screen_middle_width}+{screen_middle_height}")
    #puts a label that lets user know what the following textbook is for
    tk.Label(feedback_window, text = "Please enter any feedback you have for us!").pack(pady = 5)
    #creates a textbook (better than entry because it takes in multiple lines)
    feedback_text = tk.Text(feedback_window, width = 50, height = 8)
    feedback_text.focus()
    #this gives 5 pixels of vertical padding
    feedback_text.pack(pady = 5)
    
    def submit_feedback():
        #feedback is retrieved from feedback window (from first to the final character), and uses .strip() to remove whitespace
        #in tkinter the first character of a tk.Text widget is "1.0" (first line, first character)
        feedback = feedback_text.get("1.0", tk.END).strip()
        #if feedback is a string, it automaticall evaluates as true
        if feedback:
            try:
                #opens and reads the file and uses json,load()
                with open("feedback.json", "r") as file:
                    data = json.load(file)
            except FileNotFoundError:
                #creates a new list that stores data[] if the file is not found
                data = []
            #appends the data in a dictionary for readability
            data.append({"feedback" : feedback})
            #opens the file and rewrites the new appended object
            with open("feedback.json", "w") as file:
                json.dump(data, file, indent = 4)
            #shows a confirmation that feedback has been recieved
            messagebox.showinfo("Thank You", "Thank you, your feedback has been recieved!")
            #destroys this window
            feedback_window.destroy()
            #shows the root again
            root.deiconify()
        else:
            messagebox.showwarning("Empty", "Please type in some feedback before submitting!")

    def on_close():
        cancel_feedback = messagebox.askokcancel("Cancel feedback", "Do you want to cancel your feedback?")
        if cancel_feedback:
            feedback_window.destroy()
            root.deiconify()
        
    #this button is the submit button and will run the command submit_feedback when clicked
    tk.Button(feedback_window, text = "Submit", command = submit_feedback).pack(side = "left", padx = 20, pady = 10)
    #this button is the cancel button and will run a lambda (anonymous) function that destroys the feed_backwindow and shows the root again
    tk.Button(feedback_window, text = "Cancel", command = lambda : [feedback_window.destroy(), root.deiconify()]).pack(side = "right", padx = 20, pady = 10)
    feedback_window.protocol("WM_DELETE_WINDOW", on_close)

#creates button with the callback function get_values, columnspan of 2 means it is the width of 2 columns
tk.Button(frame, text = "SUBMIT", command = get_values).grid(row = 4, column = 0, padx = 10, pady = 10)
#creates exit button
#on button click, lambda (function without name) runs sys.exit()
#lambda functions are very efficient if they are short functions (e.g one lined)
#sys.exit() is necessary to stop all execution
tk.Button(frame, text = "EXIT", command = lambda : sys.exit()).grid(row = 4, column = 1, padx = 10, pady = 10)
#creates feedback button
tk.Button(frame, text = "FEEDBACK", command = get_feedback).grid(row = 4, column = 2, padx = 10, pady = 10)
root.mainloop()

#die_1 = Die(6)
#result = die_1.roll_dice(100)
#frequencies = die_1.get_frequencies(result)
#we pass result because we calculate frequencies in get_frequencies
#die_1.create_histogram(result)
#die_1.visualize_scatter(result)
#more examples
#uses a try except to provide a user friendly message

try: 
    die_2 = Die(dice_info[0])
    die_3 = Die(dice_info[1])
    game = DiceGameRoll([die_2, die_3])
    #dice_values[-1] will always give the last value in the list
    rolls = game.roll_all(dice_info[-1])
    #reminder -take a look at this later because the index error gets called even when the list is populated
except IndexError:
    #informs the user of an index error where the list is not populated
    messagebox.showwarning("Index Error", "Index Error, list is not populated")
    #gives the user the option to use default dice sides or cancel
    #answer can either be the boolean true (Yes) or False (Cancel / No)
    answer = messagebox.askyesnocancel("Option", "Use default dice sides (6) or cancel?")
    if answer:
        die_2, die_3 = Die(), Die()
        game = DiceGameRoll([die_2, die_3])
        rolls = game.roll_all()
    else:
        #cancels if the user chooses to cancel
        messagebox.showinfo("Cancelled", "Dice simulation cancelled")
#uses a try except block to handle exceptions without getting error messages
#in this case this error occurs when the user cancels the dice simulation
try:
    #the two dices are passed in because the parameter requires a list
    products = game.get_product(rolls)
    sums = game.get_sum(rolls)
    possible_products = game.get_all_possible_products()
    possible_sums = game.get_all_possible_sums()
    roll_frequencies = game.get_frequencies(rolls, "sum")
    #game.visualize_histogram_data(rolls)
    #game.visualize_histogram_data(rolls, "dice_products.svg", "product")
    game.visualize_scatter_data(rolls)
    game.visualize_scatter_data(rolls, "product")
    game.compare_scatter_data(rolls)
    key_features = game.get_key_features(rolls)
    game.save_data(rolls)
    game.clear_file_data()
#name error exception is passed so the user doesn't experience too many error messages
except NameError:
    pass
        #messagebox.showwarning("Error", "Name not defined")