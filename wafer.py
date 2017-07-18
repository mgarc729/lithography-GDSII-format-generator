import numpy
import pilar as Pilar
from tools import generate_circle_points as gc
import gdspy

class Wafer:
    SIZE_2_IN= 50
    SIZE_4_IN = 100
    SIZE_8_IN = 150
    SIZE_16_IN = 300
    
    SIZES = [SIZE_2_IN, SIZE_4_IN, SIZE_8_IN, SIZE_16_IN]

    _MM_IN_MICRONS = 1000 #the value of one mm in microns (1mm = 1000um)
    
    _ANGLES = {SIZE_4_IN:71.03}
    _FLAT_FRAGMENTS = {SIZE_4_IN: 15.4}

    _ZERO_DEGREES = 0
    _180_DEGREES = 180
    
    _ONE_DIV = 1
    _TWO_DIV = 2
    _FOUR_DIV = 4

    WAFER_LAYER = 1
    MARGIN_LAYER = 2
    STRUCTURES_LAYER = 3

    MICRONS = 1.0e-6
    NANOMETERS = 1.0e-9

    UNITS = [MICRONS, NANOMETERS]

    DIVISIONS = [_ONE_DIV, _TWO_DIV, _FOUR_DIV]

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
        self.flat_fragment = self._FLAT_FRAGMENTS[size]
        self.size = size * self._MM_IN_MICRONS
        self.margin = margin * self._MM_IN_MICRONS
        self.unit = unit
        self.precision = precision
        self.cell = gdspy.Cell(cell_name)

        self._create_main_shape()
        self._create_margin_shape()
        
        self.filename = filename


        self.sections = self._ONE_DIV 

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

    def write(self):
        gdspy.write_gds('{0}.gds'.format(self.filename), unit=self.unit, precision=self.precision)

    def partition(self, divisions):
        """
        This method partitions the wafer into rows and columns and
        enumerates them.

        """
        if divisions  not in self.DIVISIONS:
            raise ValueError("It must be a valid division: {0}".format(self.DIVISIONS))
        
        self.sections = divisions
        

    def generate_pilars(self, distance, radius, overhang, section=1):
        if section not in range(1, self.sections + 1):
            raise ValueError("Selected Section has to be positive and less or equal to {0}".format(self.sections));
        
        total_radius = radius + overhang

        if self.sections == self._ONE_DIV:
            x = -self.size/2
            y = self.size/2
            
            pilars_polygons = []
            pilars = Pilar.generate_pilars_region(  distance,
                                                    radius, 
                                                    x, 
                                                    y, 
                                                    self.size, 
                                                    self.size)
            for pilar in pilars:
                poly = gdspy.Polygon(pilar, self.STRUCTURES_LAYER)
                pilars_polygons.append(poly)
                #self.cell.add(poly)

            merged = gdspy.fast_boolean(pilars_polygons, self.margin_polygon, 'and', layer=self.STRUCTURES_LAYER,max_points=0)
            self.cell.add(merged)
