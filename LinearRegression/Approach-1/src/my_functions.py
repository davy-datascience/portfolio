import numpy as np
import matplotlib.pyplot as plt
from sympy.geometry import Point, Line

def drawAll(X, Y, line):
    """ plot the points from the dataset and draw the actual Line """
    coefs = line.coefficients
    x = np.linspace(X.min(),X.max())
    y = (-coefs[0] * x - coefs[2]) / coefs[1]
    plt.plot(x, y)
    plt.scatter(X, Y, color = 'red')
    plt.show()

def transformLine(point, line, x_median, learning_rate): 
    """ According to the random point, update the Line """
    # We take the median of the x values for better results for the calculations of the horizontal distances
    
    # Creation of the vertical line passing through the new point
    ymin = line.points[0] if line.direction.y > 0 else line.points[1]
    ymax = line.points[1] if line.direction.y > 0 else line.points[0]
    vertical_line = Line(Point(point.x,ymin.y), Point(point.x,ymax.y))
    # Find the intersection with our line (to calculate the vertical distance)
    I = line.intersection(vertical_line)
    vertical_distance = point.y - I[0].y
    horizontal_distance = point.x - x_median  
    
    coefs = line.coefficients

    a = coefs[0]
    b = coefs[1]
    c = coefs[2]
    
    # Calculation of the points which constitute the new line
    # Reminder: we add (learning_rate * vertical_distance * horizontal_distance) to the slope and we add (learning_rate * vertical_distance) to y-intercept
    # The equation now looks like : 
    # y = - (a/b)*x + (learning_rate * vertical_distance * horizontal_distance) * x - (c/b) + learning_rate * vertical_distance

    # We keep the same scope of the line so the min value of x and the max value of x don't change
    
    x_min = line.points[0].x
    y_min = - (a/b)*x_min + (learning_rate * vertical_distance * horizontal_distance * x_min) - (c/b) + learning_rate * vertical_distance
    
    x_max = line.points[1].x
    y_max = - (a/b)*x_max + (learning_rate * vertical_distance * horizontal_distance * x_max) - (c/b) + learning_rate * vertical_distance
    
    newLine = Line(Point(x_min, y_min), Point(x_max, y_max))
    return newLine
    
def predict(X, line):
    """ I use my model (the equation of the line) to predict new values """
    prediction = []
    coefs = line.coefficients
    a = coefs[0]
    b = coefs[1]
    c = coefs[2]
    for x in X.values:
        y = - (a/b)*x - (c/b)
        prediction.append(y)
    return prediction