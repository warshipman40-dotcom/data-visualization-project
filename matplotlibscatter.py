import matplotlib.pyplot as plt
x_values = [1, 2, 3, 4, 5]
y_values = []
#sets size of dots as 200 at the coordinates x_values, y_values
for x in x_values:
    y_values.append(x ** 2)
#custom colors can be created values closer to 0 will be darker, while closer to 1 will be lighter
#plt.scatter(x_values, y_values, c=(0, 1.0, 0.9), edgecolors="blue", s = 100)
#a colormap can also be used
#passes the list of y-values to use
plt.scatter(x_values, y_values, c = y_values, cmap=plt.cm.Blues, edgecolors="none", s= 40)
plt.show()

#set chart title and label axes.
plt.title("Square Numbers", fontsize = 24)
plt.xlabel("Value", fontsize = 14)
plt.ylabel("Square of Value", fontsize = 14)

#sets size of tick labels.

plt.tick_params(axis = "both", which = "major", labelsize = 14)