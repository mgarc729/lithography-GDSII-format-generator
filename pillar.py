import numpy as np

from tools import generate_circle_points as gc

def generate_pilars_positions(distance, radius, x, y, width, height):
    """Calculates the position of the pilars within the drawing area.

    Args:
        distance: Distance from the center of one pillar to the center
                    of an adjacent one.
        radius: Distance from the center of the pillar to the edge.
        x: x coordinate of the rectangular drawing area.
        y: y coordinate of the rectangular drawing area.
        width: width of the rectangular drawing area.
        height: height of the rectangular drawing area.
        
    """
    pair_distance = (2 * radius) + (distance - 2*radius)
        
    pilars_x_axis = int(width / pair_distance)
    pilars_y_axis = int(height / pair_distance)

    gap_x_axis = (width - (pilars_x_axis * pair_distance))/2 + radius#gap both sides of the rectangle
    gap_y_axis = (height - (pilars_y_axis * pair_distance))/2 + radius

    points = [] #set of positions
    for col in range(0, pilars_x_axis):
        for row in range(0, pilars_y_axis):
            points.append(( (x + gap_x_axis) + col*pair_distance,
                                (y - gap_y_axis) - row*pair_distance))
    return points

def generate_pilars_region(distance, radius, x,y,width, height):
    """Generate Pillar structures in a specific area.
    
    Args:
        distance: Distance from the center of one pillar to the center
                    of an adjacent one.
        radius: Distance from the center of the pillar to the edge.
        x: x coordinate of the rectangular drawing area.
        y: y coordinate of the rectangular drawing area.
        width: width of the rectangular drawing area.
        height: height of the rectangular drawing area.
    """

    points = generate_pilars_positions(distance, radius, x, y, width, height)

    # The template is a circle located at 0,0 and with the specific radius
    # calculating this once save a lot of time. Then we only need to transale
    # the template.
    template_x, template_y = gc(radius, 0, 360, 100)
    pilars = []
    
    for point in points:
        pilars.append(zip(  template_x + point[0],
                                template_y + point[1]))
    return pilars

