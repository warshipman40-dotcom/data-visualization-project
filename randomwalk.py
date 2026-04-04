import matplotlib.pyplot as plt
from random_walk import RandomWalk

#make a random walk and plots the points
#keeps making new walks as long as program is active
while True:
    rw = RandomWalk(50000)
    rw2 = RandomWalk(5000)
    rw2.fill_walk()
    rw.fill_walk()
    #creates a list with the total nmber of points
    point_numbers = list(range(rw.num_points))
    #this results in a plot of the walk that ranges in a gradient of blue
    #plt.scatter(rw.x_values, rw.y_values, c = point_numbers, cmap=plt.cm.Blues, edgecolors="none", s = 1)
    plt.plot(rw2.x_values, rw2.y_values, lw = 1.25)
    
    #emphasizes the first and last points
    #plt.scatter(0, 0, c="green", edgecolors="none", s=100)
    #plt.scatter(rw.x_values[-1], rw.y_values[-1], c="red", edgecolors="none", s= 100)
    
    #removes the axes using the plt.gca() function
    #gca gets the current axes
    plt.gca().get_xaxis().set_visible(False)
    plt.gca().get_yaxis().set_visible(False)
    plt.figure(figsize = (10, 6))
    plt.show()
    keep_running = input("Make another walk? (y/n):")
    if keep_running == "n":
        break

# %%



