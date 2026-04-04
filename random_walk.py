from random import choice
class RandomWalk():
    """A Class to generate randoms walks"""
    #total number of points on walk, sets default of 5000
    def __init__(self, num_points = 5000):
        """Initialize the attributes of a walk"""
        self.num_points = num_points

        #Ensures wall walks start at (0, 0)
        self.x_values = [0]
        self.y_values = [0]

    #runs until the walk is filled with the correct number of points
    def fill_walk(self):
        """Calcualte all the points in the walk"""
        #keep taking steps until the walk reeaches the desired length
        while len(self.x_values) < self.num_points:
            x_step = self.get_step()
            y_step = self.get_step()
            #rejects moves that go nowhere
            if x_step == 0 and y_step == 0:
                continue
            #gets next value for walk by adding the value in x_step to the last value stored in x_value and same for y_values
            next_x = self.x_values[-1] + x_step
            next_y = self.y_values[-1] + y_step

            self.x_values.append(next_x)
            self.y_values.append(next_y)

    def get_step(self):
        #Decides which direction to go and how far to go in that direction
        direction = choice([1, -1])
        distance = choice([0, 1, 2, 3, 4, 5, 6, 7])
        return direction * distance

