import numpy as np
import gdspy


def create_circle_polygons(radius,initial_angle, final_angle, points=199):

    theta = np.linspace(np.deg2rad(initial_angle), np.deg2rad(final_angle), points)
    a, b = radius * np.cos(theta) , radius * np.sin(theta) 
    
    return a,b

def generate_array_pilars(distance, radius, overhang, number_rows, number_columns):
    """
        This methods generates the center point of the pilars
    """
    
    pilar_total_radius = overhang + radius

    if 2*pilar_total_radius > distance:
        raise ValueError("The combine size of two adjacent pilars can't be greater than the distance bewtween them");
    

    left_boundary = -1 * ((number_columns + 1)/2) * distance
    top_boundary = -1 * ((number_rows + 1)/2) * distance

    set_of_points = []

    for row in range(0,number_rows):
        for col in range(0, number_columns):
            set_of_points.append((left_boundary + col*distance, top_boundary + row*distance))

    return set_of_points
def generate_grid(distance, thickness, number_rows, number_cols, width, height):

    grid_cell = gdspy.Cell('GRID')
    total_horizontal_gap = (number_cols - 1) * distance + thickness
    total_vertical_gap = (number_rows - 1)* distance + thickness

    horizontal_left = width - total_horizontal_gap
    vertical_left = height - total_vertical_gap

    horizontal_margin = horizontal_left/ 2
    vertical_margin = vertical_left / 2

    horizontal_start = -width/2 + horizontal_margin
    vertical_start = height/2 - vertical_margin
    
    vertical_bars = []
    horizontal_bars = []

    for col in range(0, number_cols):
        bar = gdspy.Rectangle((horizontal_start + col*distance,height/2),(horizontal_start + col*distance + thickness, -height/2),1)
        #grid_cell.add(bar)
        vertical_bars.append(bar)

    for row in range(0, number_rows):
        bar = gdspy.Rectangle((-width/2, vertical_start - row*distance),(width/2, vertical_start - row*distance - thickness),1)
        #grid_cell.add(bar)
        horizontal_bars.append(bar)

    merged = gdspy.fast_boolean(vertical_bars, horizontal_bars, 'or', layer=1,max_points=0)
    """
    merged = None
    for vertical in vertical_bars:
        for horizontal in horizontal_bars:
            merged = gdspy.fast_boolean(merged, horizontal, 'or', max_points=0)
            merged = gdspy.fast_boolean(merged, vertical, 'or', max_points=0)
    """
    grid_cell.add(merged)
    gdspy.write_gds('grid.gds', unit=1.0e-6, precision=1.0e-9)

def generate_grid_copy(distance, thickness, number_rows, number_cols, width, height):

    grid_cell = gdspy.Cell('GRID')
    total_horizontal_gap = (number_cols - 1) * distance + thickness
    total_vertical_gap = (number_rows - 1)* distance + thickness

    horizontal_left = width - total_horizontal_gap
    vertical_left = height - total_vertical_gap

    horizontal_margin = horizontal_left/ 2
    vertical_margin = vertical_left / 2

    horizontal_start = -width/2 + horizontal_margin
    vertical_start = height/2 - vertical_margin
    
    vertical_bars = []
    horizontal_bars = []
    squares = []
    for col in range(0, number_cols):
        for row in range(0, number_rows):
            x = horizontal_start+thickness + col*(distance + thickness)
            y = vertical_start + thickness - row*(distance + thickness)        
            square = gdspy.Rectangle((x,y),(x + distance, y - distance),1)
            #grid_cell.add(square)
            squares.append(square)

    """
    for col in range(0, number_cols):
        bar = gdspy.Rectangle((horizontal_start + col*distance,height/2),(horizontal_start + col*distance + thickness, -height/2),1)
        #grid_cell.add(bar)
        vertical_bars.append(bar)

    for row in range(0, number_rows):
        bar = gdspy.Rectangle((-width/2, vertical_start - row*distance),(width/2, vertical_start - row*distance - thickness),1)
        #grid_cell.add(bar)
        horizontal_bars.append(bar)
    """
    area = gdspy.Rectangle((height/2, -width/2),(-height/2,width/2),1)
    merged = gdspy.fast_boolean(area,squares, 'not', max_points=0)
   # merged = gdspy.fast_boolean(vertical_bars, horizontal_bars, 'or', max_points=0)
    grid_cell.add(merged)
    gdspy.write_gds('grid.gds', unit=1.0e-6, precision=1.0e-9)


def create_wafer(cell, margin):
    a, b = create_circle_polygons(1000 * 100, -71.03, 180 + 71.03,300)
    cell.add(gdspy.Polygon(zip(a,b),2))
    a, b = create_circle_polygons(1000 * (100 - margin), -71.03, 180 + 71.03,300)
    cell.add(gdspy.Polygon(zip(a,b),3))

def populate_dgs_file(filename, radius, overhang,array_of_points):
    pilars_cell = gdspy.Cell('PILLARS')

    create_wafer(pilars_cell, 5)

    pilar_total_radius = radius + overhang
    a,b = create_circle_polygons(pilar_total_radius,0,360)
    for point in array_of_points:
        points = zip(a + point[0], b + point[1])
        pilars_cell.add(gdspy.Polygon(points, 1))
        
    gdspy.write_gds('{0}.gds'.format(filename), unit=1.0e-6, precision=1.0e-9)

    #gdspy.LayoutViewer()

def generate_dsg_file(filename,distance, radius, overhang, number_rows, number_columns):
    array_of_points = generate_array_pilars(distance, radius, overhang, number_rows, number_columns)
    populate_dgs_file(filename,radius, overhang, array_of_points)

def main():
    generate_grid(10,2,10,10,150,150)


if __name__ == "__main__":
    main()
