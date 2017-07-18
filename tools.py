import numpy as np


def generate_circle_points(radius, initial_angle, final_angle, points=199):
    """
    This methods generates points in a circle shape at (0,0) with a specific radius and from a 
    starting angle to a final angle.

    Arguments:
        radius: radius of the circle in microns
        initial_angle: initial angle of the drawing in degrees
        final_angle: final angle of the drawing in degrees
        points: amount of points to be generated
    """
    theta = np.linspace(    np.deg2rad(initial_angle), 
                            np.deg2rad(final_angle), 
                            points)

    return  radius * np.cos(theta) , radius * np.sin(theta) 
    
    


