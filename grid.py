import numpy as np

def generate_grid_region(distance, thickness, x, y, width, height): 
    """Generate Grid structures in a specific area.
    
    Args:
        distance: Distance from the center of one "wall" to the other.
        radius: Distance from one edge of the "wall" to the other.
        x: x coordinate of the rectangular drawing area.
        y: y coordinate of the rectangular drawing area.
        width: width of the rectangular drawing area.
        height: height of the rectangular drawing area.

    return:
        (horizontal_points, vertical_points): Set of points in each 
            direction.
    """

    pair_distance = thickness + (distance - thickness)

    walls_x_axis = int(width / pair_distance)
    walls_y_axis = int(height / pair_distance)

    # Calculating the gap on each side to fit the structure right in the
    # middle of the area
    gap_x_axis = (width - (walls_x_axis * pair_distance))/2 #gap both sides of the rectangle
    gap_y_axis = (height - (walls_y_axis * pair_distance))/2
        
    # Each "wall" is a rectangle determined by 2 coordinates in oposite vertices    
    horizontal_points = []
    vertical_points = []

    for col in range(0, walls_x_axis):
        corner = x + gap_x_axis + col*distance
        horizontal_points.append(((corner, y),(corner + thickness, y - height)))

    for row in range(0, walls_y_axis):
        corner = y - gap_y_axis - row*distance
        vertical_points.append(((x , corner),(x + width,corner - thickness)))

    return (horizontal_points, vertical_points)
