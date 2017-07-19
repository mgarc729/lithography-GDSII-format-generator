import numpy
import pillar as Pillar
import grid as Grid
from tools import generate_circle_points as gc
import gdspy

class Wafer:
    SIZE_2_IN= 51
    SIZE_4_IN = 100
    SIZE_6_IN = 150
    SIZE_8_IN = 200
        
    SIZES = [SIZE_2_IN, SIZE_4_IN, SIZE_6_IN, SIZE_8_IN]

    _MM_IN_MICRONS = 1000 #the value of one mm in microns (1mm = 1000um)
    
    _ANGLES = {SIZE_4_IN:71.03}
    _FLAT_FRAGMENTS = {SIZE_4_IN: 47.28}

    _ZERO_DEGREES = 0
    _180_DEGREES = 180

    WAFER_LAYER = 1
    MARGIN_LAYER = 2
    STRUCTURES_LAYER = 3

    MICRONS = 1.0e-6
    NANOMETERS = 1.0e-9
    
    GAP_BETWEEN_SECTIONS = 1 * _MM_IN_MICRONS

    UNITS = [MICRONS, NANOMETERS]
    
    PILLARS = 'Pillars'
    GRID = 'Grid'

    def __init__(self,size, margin, filename="mask", unit=MICRONS, precision=NANOMETERS, cell_name = "WAFER"):
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

        self._create_main_shape()
        self._create_margin_shape()
        self._create_drawing_area() 
        self.filename = filename
        
        self.rows = 1
        self.cols = 1
        self.num_sections = 1

        self.setups = {}

    def _create_main_shape(self):
        a, b = gc( self.size/2,
                self._ZERO_DEGREES - self.angle,
                self._180_DEGREES + self.angle)
        self.wafer_points = zip(a,b)
        self.wafer_polygon = gdspy.Polygon(self.wafer_points, self.WAFER_LAYER)
        self.cell.add(self.wafer_polygon)

    def _create_margin_shape(self):
        a, b = gc(  (self.size/2 - self.margin),
                self._ZERO_DEGREES - self.angle,
                self._180_DEGREES + self.angle)
        self.margin_points = zip(a,b)
        self.margin_polygon = gdspy.Polygon(self.margin_points, self.MARGIN_LAYER)
        self.cell.add(self.margin_polygon)
    
    def _create_drawing_area(self):
        self.drawing_x = -self.size/2 + self.margin
        self.drawing_y = self.size/2 - self.margin
        self.drawing_width = self.size - self.margin * 2
        self.drawing_height = (self.size/2 + self.flat_fragment) - self.margin * 2
        
        self.drawing_x_step = self.drawing_width 
        self.drawing_y_step = self.drawing_height

    def write(self):
        gdspy.write_gds('{0}.gds'.format(self.filename), unit=self.unit, precision=self.precision)

    def partition(self, rows, cols):
        """
        This method partitions the wafer into rows and columns and
        enumerates them.

        """
        self.num_sections = rows * cols
        self.cols = cols
        self.rows = rows
        
        self.drawing_x_step = int(self.drawing_width/cols)
        self.drawing_y_step = int(self.drawing_height/rows)


    def generate_section_structures(self, distance, radius, structure = PILLARS, section=1):
        if section > self.num_sections:
            raise ValueError("Selected Section has to be less or equal than {0}".format(self.num_sections));
        
        row = int((section - 1) / self.cols)
        col = int((section - 1) % self.cols)
        
        x = self.drawing_x + col * self.drawing_x_step
        y = self.drawing_y - row * self.drawing_y_step
        
        
        width = self.drawing_x_step - self.GAP_BETWEEN_SECTIONS/2
        height = self.drawing_y_step - self.GAP_BETWEEN_SECTIONS/2

        polygons = []
        if structure == self.PILLARS:
            pilars = Pillar.generate_pilars_region(  distance,
                                                    radius, 
                                                    x, 
                                                    y, 
                                                    width, 
                                                    height)

            for pilar in pilars:
                poly = gdspy.Polygon(pilar, self.STRUCTURES_LAYER)
                polygons.append(poly)

        elif structure == self.GRID:
            horizontal, vertical = Grid.generate_grid_region(  distance,
                                                    radius, 
                                                    x, 
                                                    y, 
                                                    width, 
                                                    height)
            for h in horizontal:
                poly = gdspy.Rectangle(h[0], h[1], self.STRUCTURES_LAYER )
                polygons.append(poly)
            
            for v in vertical:
                poly = gdspy.Rectangle(v[0], v[1], self.STRUCTURES_LAYER )
                polygons.append(poly)
        self.setups[section] = {'radius':radius, 'distance':distance, 'structure':structure}
        merged = gdspy.fast_boolean(polygons, self.margin_polygon, 'and', layer=self.STRUCTURES_LAYER,max_points=3000)
        self.cell.add(merged)

    def add_setup(self, distance, radius, structure=PILLARS, section=1):
        if section > self.num_sections:
            raise ValueError("Selected Section has to be less or equal than {0}".format(self.num_sections));
        self.setups[section] = {'radius':radius, 'distance':distance, 'structure':structure}

    def generate_setups(self):
        for section, setup in self.setups.iteritems():
            self.generate_section_structures(setup['distance'],
                                                setup['radius'],
                                                setup['structure'],
                                                section)
        self.write()









