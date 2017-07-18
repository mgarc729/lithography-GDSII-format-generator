import numpy as np

def generate_grid_region(distance, thickness, x, y, width, height):
    pair_distance = thickness + (distance - thickness)

    walls_x_axis = int(width / pair_distance)
    walls_y_axis = int(height / pair_distance)


    gap_x_axis = (width - (walls_x_axis * pair_distance))/2 #gap both sides of the rectangle
    gap_y_axis = (height - (walls_y_axis * pair_distance))/2
        
    horizontal_points = []
    vertical_points = []

    for col in range(0, walls_x_axis):
        corner = x + gap_x_axis + col*distance
        horizontal_points.append(((corner, y),(corner + thickness, y - height)))

    for row in range(0, walls_y_axis):
        corner = y - gap_y_axis - row*distance
        vertical_points.append(((x , corner),(x + width,corner - thickness)))

    return (horizontal_points, vertical_points)
