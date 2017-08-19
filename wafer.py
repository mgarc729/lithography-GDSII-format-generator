import numpy
import gdspy

from tools import generate_circle_points as gc
import pillar as Pillar
import grid as Grid


class Wafer:
    """Handles all the processes of modeling on a wafer shape.

    This class allows the user to create a gds template of the desired
    wafer size (2,4,6,8 in). It provides tools to partition the wafer
    in sections by specifying the number of rows and columns that the
    wafer needs to be partitioned. Sections are enumerated from left to 
    right, top to bottom,  starting at section number 1. 

    Example (3 rows and 3 cols)
    
    |-----------|
    | 1 | 2 | 3 |
    |---|---|---|
    | 4 | 5 | 6 |
    |---|---|---|
    | 7 | 8 | 9 |
    |-----------|
    
    There are two types of structures that can be generated: Pillars and 
    Grid. 

    Atributes:
        size: Current size of the wafer in Microns.
        margin: Current margin from the edge of the wafer to the
                drawing area in Microns.
        unit: Scale of the drawing (default MICRONS)
        precision: Minimum division (default NANOMETERS)
        rows: Number of partitions horizontally (default 1)
        cols: Number of partitions vertically (default 1)
        num_partitions: Total number of partitions (rows*cols) (default 1)
        setups: Each partition has a different setup that depends on the
                structures and the properties, setups[n] provides the setup
                for partition n.
                Each setup provides:
                    setup['distance']
                    setup['radius']
                    setup['structure']
            
    Raises:
        ValueError: If the specified wafer size is not listed or
                    if the units or precision are not listed or
                    if precision is larger than units.
    """
    

    # Different wafer sizes
    SIZE_2_IN= 51
    SIZE_4_IN = 100
    SIZE_6_IN = 150
    SIZE_8_IN = 200
        
    SIZES = [SIZE_2_IN, SIZE_4_IN, SIZE_6_IN, SIZE_8_IN]

    # Thevalue of one mm in microns (1mm = 1000um)
    _MM_IN_MICRONS = 1000 
   
    # Each wafer has a different starting and ending angle
    # where the flat mark is.
    _ANGLES = {SIZE_2_IN:71.86, SIZE_4_IN:71.03, SIZE_6_IN: 67.46}
    _FLAT_FRAGMENTS = {SIZE_2_IN: 24.23, SIZE_4_IN: 47.28, SIZE_6_IN: 69.27}

    _ZERO_DEGREES = 0
    _180_DEGREES = 180

    # Different layers of Data
    WAFER_LAYER = 1
    MARGIN_LAYER = 2
    STRUCTURES_LAYER = 3

    # Units used
    MICRONS = 1.0e-6
    NANOMETERS = 1.0e-9
    
    UNITS = [MICRONS, NANOMETERS]

    # Avoiding Sections to be closed to eachother
    GAP_BETWEEN_SECTIONS = 1 * _MM_IN_MICRONS

    # Structures that can be generated
    PILLARS = 'Pillars'
    GRID = 'Grid'
    LINES_V = 'Lines V'
    LINES_H = 'Lines H'
    
    STRUCTURES = [PILLARS, GRID, LINES_V, LINES_H]

    DEFAULT_FILENAME = 'mask'

    def __init__(self,size, margin, unit=MICRONS, precision=NANOMETERS, cell_name = "WAFER"):
        if size  not in self.SIZES:
            raise ValueError("The wafer must be a valid size: {0}".format(self.SIZES))
        
        if unit not in self.UNITS:
            raise ValueError("Unit has to be a valid one: {0}".format(self.UNITS))

        if precision not in self.UNITS:
            raise ValueError("Precision has to be a valid one: {0}".format(self.UNITS))

        if precision > unit:
            raise ValueError("Precision has to be smaller than unit")

        self.angle = self._ANGLES[size]
        self.flat_fragment = self._FLAT_FRAGMENTS[size] * self._MM_IN_MICRONS
        self.size = size * self._MM_IN_MICRONS
        self.margin = margin * self._MM_IN_MICRONS
        self.unit = unit
        self.precision = precision
        self.cell = gdspy.Cell(cell_name)
        self.cell_name = cell_name
        
        self._create_drawing_area() 
        self.rows = 1
        self.cols = 1
        self.num_sections = 1

        self.setups = {}

    def _create_main_shape(self):
        """Creates the wafer shape in the file."""

        a, b = gc( self.size/2,
                self._ZERO_DEGREES - self.angle,
                self._180_DEGREES + self.angle)
        self.wafer_points = zip(a,b)
        self.wafer_polygon = gdspy.Polygon(self.wafer_points, self.WAFER_LAYER)
        self.cell.add(self.wafer_polygon)

    def _create_margin_shape(self):
        """Creates the margin shape in the file.

        Depending on the chosen margin the margin shape is gonna be
        margin units away from the wafer shape.
        """

        a, b = gc((self.size/2 - self.margin),
                   self._ZERO_DEGREES - self.angle,
                   self._180_DEGREES + self.angle)
        self.margin_points = zip(a, b)
        self.margin_polygon = gdspy.Polygon(self.margin_points, self.MARGIN_LAYER)
        self.cell.add(self.margin_polygon)
    
    def _clear_library(self):
        gdspy.Cell.cell_dict.pop(self.cell_name)
        del self.cell

    def _create_drawing_area(self):
        """Creates a rectangular shape fits the margin area in it.

        This area is the one that gets partitioned into sections. 
        each of the rectangles then gets merged with the margin 
        area in order to have a perfect fit in the wafer and 
        respecting the margin chosen.
        """

        self.drawing_x = -self.size/2 + self.margin
        self.drawing_y = self.size/2 - self.margin
        self.drawing_width = self.size - self.margin * 2
        self.drawing_height = (self.size/2 + self.flat_fragment) - self.margin * 2
        
        self.drawing_x_step = self.drawing_width 
        self.drawing_y_step = self.drawing_height

    def write(self, filename=DEFAULT_FILENAME):
        """Saves the generated structures.
        
        Args:
            filename: name of the file to be saved ommiting the .gds extension.
        """

        gdspy.write_gds('{0}.gds'.format(filename), unit=self.unit, precision=self.precision)

    def partition(self, rows, cols):
        """Partitions the drawing area into the specified rows and colums.
        
        Args:
            rows:int The number of rows that the wafer is going to be partition into.
            cols:int The number of rows that the wafer is going to be partition into.

        Raise:
            ValueError: If either row and cols arguments are not integers.
        """
        if not isinstance(rows, int) or not isinstance(cols, int):
            raise ValueError("The number of rows and columns has to be integers.")

        self.num_sections = rows * cols
        self.cols = cols
        self.rows = rows
        
        self.drawing_x_step = int(self.drawing_width/cols)   # Width of each section
        self.drawing_y_step = int(self.drawing_height/rows)  # Height of each section

    def change_wafer_size(self, size):
        """Changes the size of the actual wafer.
            
        Args:
            size: new size of the wafer

        Raise:
            ValueError: If the size is not in the list of possible wafer sizes
        """
        if size not in self.SIZES:
            raise ValueError("The wafer must be a valid size: {0}".format(self.SIZES))
        
        self.size = size * self._MM_IN_MICRONS

        self._create_drawing_area()
        self.partition(self.rows, self.cols)

    def change_margin(self, margin):
        """
        Changes the margin size of the wafer

        This method changes the margin size of the wafer. It determines the area where the structures are gonna be
        generated. There are no structures that fall outside the area described by the margin.

        :param margin: size in mm of the margin where the structures are gonna be drawn
        :return: void
        """
        self.margin = margin * self._MM_IN_MICRONS

        self._create_drawing_area()
        self.partition(self.rows, self.cols)

    def _generate_section_structures(self, distance, radius, structure=PILLARS, section=1):
        """Generates the desired structures in the selected section.

        Args:
            distance: In the case of pillars is the distance between their centers and in 
                      the case of grid is the distance between the middle oftwo parallel "walls".
            radius: In the case of pillars is the distance between the center and the edge. In the
                    case of grid is the distance between each edge.
            structure: Structure that is going to be generated. (default Pillars)
            section: Section where the structures are going to be generated.

        Raise:
            ValueError: If the selected section is out of range.
        """
        if section > self.num_sections:
            raise ValueError("Selected Section has to be less or equal than {0}".format(self.num_sections));
        
        row = int((section - 1) / self.cols)
        col = int((section - 1) % self.cols)
       
        # Calculating starting coordinates of the section
        x = self.drawing_x + col * self.drawing_x_step
        y = self.drawing_y - row * self.drawing_y_step

        # Correcting width and height to respect the gap
        width = self.drawing_x_step - self.GAP_BETWEEN_SECTIONS/2 
        height = self.drawing_y_step - self.GAP_BETWEEN_SECTIONS/2

        polygons = []
        if structure == self.PILLARS:
            pillars = Pillar.generate_pilars_region(distance,
                                                    radius, 
                                                    x, 
                                                    y, 
                                                    width, 
                                                    height)

            for pillar in pillars:
                poly = gdspy.Polygon(pillar, self.STRUCTURES_LAYER)
                polygons.append(poly)

        else:
            horizontal, vertical = Grid.generate_grid_region(distance,
                                                             radius,
                                                             x,
                                                             y,
                                                             width,
                                                             height)
            if structure == self.GRID:

                for h in horizontal:
                    poly = gdspy.Rectangle(h[0], h[1], self.STRUCTURES_LAYER )
                    polygons.append(poly)

                for v in vertical:
                    poly = gdspy.Rectangle(v[0], v[1], self.STRUCTURES_LAYER )
                    polygons.append(poly)

            elif structure == self.LINES_H:

                for v in vertical:
                    poly = gdspy.Rectangle(v[0], v[1], self.STRUCTURES_LAYER)
                    polygons.append(poly)
            elif structure == self.LINES_V:

                for h in horizontal:
                    poly = gdspy.Rectangle(h[0], h[1], self.STRUCTURES_LAYER)
                    polygons.append(poly)

        self.setups[section] = {'radius': radius, 'distance': distance, 'structure': structure}
        # The fitting the generated rectangular section in the Margin area
        merged = gdspy.fast_boolean(polygons, self.margin_polygon, 'and', layer=self.STRUCTURES_LAYER,max_points=3000)
        self.cell.add(merged)

    def add_setup(self, distance, radius, structure=PILLARS, section=1):
        """Sets the type of structure and properties per section.
            
        Args:
            distance: In the case of pillars is the distance between their centers and in 
                      the case of grid is the distance between the middle oftwo parallel "walls".
            radius: In the case of pillars is the distance between the center and the edge. In the
                    case of grid is the distance between each edge.
            structure: Structure that is going to be generated. (default Pillars)
            section: Section where the structures are going to be generated.

        Raise:
            ValueError: If the selected section is out of range.
        """

        if section > self.num_sections:
            raise ValueError("Selected Section has to be less or equal than {0}".format(self.num_sections));
        
        if section > self.num_sections:
            raise ValueError("Selected Section has to be less or equal than {0}".format(self.num_sections));
        self.setups[section] = {'radius':radius, 'distance':distance, 'structure':structure}

    def generate_setups(self,filename=DEFAULT_FILENAME):
        """Creates every setup in the file."""
        
        self._create_main_shape()
        self._create_margin_shape()

        for section, setup in self.setups.iteritems():
            self._generate_section_structures(setup['distance'],
                                              setup['radius'],
                                              setup['structure'],
                                              section)
        self.write(filename)








