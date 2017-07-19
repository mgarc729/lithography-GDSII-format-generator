import tkinter as tk
#import generator as generator
import ttk
from wafer import Wafer

class app_gui(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.wafer = Wafer(Wafer.SIZE_4_IN, 5)
        self.initialize()
        
        self.update_sections()
        self.section_selector_cmb.current(0)
        



    def generate(self):
        self.wafer.generate_setups()

    def generate_sections(self):
        number_rows = int(self.rows_ent.get())
        number_cols = int(self.cols_ent.get())
        
        self.wafer.partition(number_rows, number_cols)
        self.update_sections()

    def section_changed(self, something):

        
        section = int(self.selected_section.get())
        setup = None
        self.radius_ent.delete(0, tk.END)
        self.distance_ent.delete(0,tk.END)
            
        try:
            setup = self.wafer.setups[section]
            self.radius_ent.insert(0,str(setup['radius']))
            self.distance_ent.insert(0,str(setup['distance']))
        except Exception:
            self.radius_ent.insert(0,'0.0')
            self.distance_ent.insert(0,'0.0')

    def save_section(self):
        section = int(self.selected_section.get())
        radius = float(self.radius_ent.get())
        distance = float(self.distance_ent.get())

        self.wafer.add_setup(distance, radius, self.wafer.PILLARS, section)

    def update_sections(self):
        self.section_selector_cmb['values'] = range(1, self.wafer.num_sections + 1)
    
    def initialize(self):
        #creating outer containers
        self.optionSection = tk.LabelFrame(self, text="Manage Sections")
        self.structureSection = tk.LabelFrame(self.optionSection, text="Structures")

        #creating labels
        self.sections_gen_lbl = tk.Label(self.optionSection, text="Sections layout:")
        self.rows_lbl = tk.Label(self.optionSection, text="Rows:")
        self.cols_lbl = tk.Label(self.optionSection, text="Columns:")

        self.filename_lbl = tk.Label(self.optionSection, text="Name of the file")

        self.section_lbl = tk.Label(self.structureSection, text="Selected Section:")
        self.distance_lbl = tk.Label(self.structureSection, text="Distance between pilars(um):")
        self.radius_lbl = tk.Label(self.structureSection, text="Base radius(um):")
        #self.overhang_lbl = tk.Label(self.structureSection, text="Overhang size (um)")
        
        #creating text fields
        self.rows_ent = tk.Entry(self.optionSection, width = 10)
        self.rows_ent.insert(0,'1')
        self.cols_ent = tk.Entry(self.optionSection, width = 10)
        self.cols_ent.insert(0,'1')

        self.filename_ent = tk.Entry(self.optionSection)

        self.distance_ent = tk.Entry(self.structureSection, width = 10)
        self.radius_ent = tk.Entry(self.structureSection, width = 10)
        #self.overhang_ent = tk.Entry(self.structureSection)
    
        #creating buttons
        self.create_file_btn = tk.Button(self.optionSection, text="Create", command=self.generate)
        self.generate_sections_btn = tk.Button(self.optionSection, text="Generate", command=self.generate_sections)
        self.save_section_btn = tk.Button(self.structureSection, text="Save", command=self.save_section)

        #creating section selector
        self.selected_section = tk.StringVar()
        self.section_selector_cmb = ttk.Combobox(self.structureSection, width=5 ,textvariable=self.selected_section)
        self.section_selector_cmb.bind('<<ComboboxSelected>>', self.section_changed)

        #adding components to the window
        self.optionSection.grid(row=0, column=0, padx=5, pady=5)
        self.sections_gen_lbl.grid(row=0, column=0, pady=5)
        self.cols_lbl.grid(row=1, column=0,padx=5, pady=5)
        self.cols_ent.grid(row=1, column=1,padx=5, pady=5)
        self.rows_lbl.grid(row=2, column=0,padx=5, pady=5)
        self.rows_ent.grid(row=2, column=1,padx=5, pady=5)
        self.generate_sections_btn.grid(row=3, column=0, padx=5, pady=5)

        self.structureSection.grid(row=4, column=0, columnspan=4, padx=5, pady=5)
        self.section_lbl.grid(row=0, column=0,padx=5, pady=5)
        self.section_selector_cmb.grid(row=0, column=1, padx=5, pady=5)
        self.distance_lbl.grid(row=1, column=0,padx=5, pady=5)
        self.distance_ent.grid(row=1, column=1,padx=5)
        self.radius_lbl.grid(row=2, column=0,padx=5, pady=5)
        self.radius_ent.grid(row=2, column=1,padx=5)
        #self.overhang_lbl.grid(row=3, column=0,padx=5, pady=5)
        #self.overhang_ent.grid(row=3, column=1,padx=5)
        self.save_section_btn.grid(row=4, column=0,padx=5, pady=5)
        
        self.filename_lbl.grid(row=5, column=0,padx=5, pady=5)

        self.filename_ent.grid(row=5, column=1,padx=5)

        self.create_file_btn.grid(row=5, column=2,padx=5, pady=5)

window = app_gui()
window.title("GDS Lithograpy mask generator")

#window.geometry("{0}x{1}+20+30".format(int(window.winfo_screenwidth()*0.75),int(window.winfo_screenheight()*0.5)))
window.mainloop()
