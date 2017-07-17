import numpy as np
import gdspy


def create_circle_polygons(x,y,radius, points=300):

    theta = np.linspace(0, 2*np.pi, points)
    a, b = radius * np.cos(theta) + x, radius * np.sin(theta) + y
    
    return zip(a,b)
 
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

def populate_dgs_file(filename, radius, overhang,array_of_points):
    pilars_cell = gdspy.Cell('PILLARS')


    pilar_total_radius = radius + overhang

    for point in array_of_points:
        pilars_cell.add(gdspy.Polygon(create_circle_polygons(point[0], point[1], pilar_total_radius), 1))
        
    gdspy.write_gds('{0}.gds'.format(filename), unit=1.0e-6, precision=1.0e-9)

    #gdspy.LayoutViewer()

def generate_dsg_file(filename,distance, radius, overhang, number_rows, number_columns):
    array_of_points = generate_array_pilars(distance, radius, overhang, number_rows, number_columns)
    populate_dgs_file(filename,radius, overhang, array_of_points)

def main():
    print generate_dsg_file(20,2,5,5,5)


if __name__ == "__main__":
    main()
