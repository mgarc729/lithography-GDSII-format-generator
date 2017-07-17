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
    print generate_dsg_file(20,2,5,5,5)


if __name__ == "__main__":
    main()
