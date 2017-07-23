import thread
import time

import tkinter as tk
import ttk
from wafer import Wafer

__version__ = '0.1.1'
__author__ = 'Manuel Garcia'

class app_gui(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.wafer = Wafer(Wafer.SIZE_2_IN, 5)
        self.initialize()
        
        self.update_sections()
       
        # Setting default values
        self.section_selector_cmb.current(0)
        self.structure_selector_cmb.current(0)
        self.wafer_size_selector_cmb.current(0)
        self.radius_ent.insert(0,'0.0')
        self.distance_ent.insert(0,'0.0')
        self.filename_ent.insert(0, self.wafer.DEFAULT_FILENAME)

    def disable_controls(self, state):
        state_text = 'normal'
        if state:
            state_text = 'disabled'

        self.create_file_btn.config(state=state_text)
        self.rows_ent.config(state=state_text)
        self.cols_ent.config(state=state_text)
        self.filename_ent.config(state=state_text)
        self.distance_ent.config(state=state_text)
        self.radius_ent.config(state=state_text)
        self.generate_sections_btn.config(state=state_text)
        self.save_section_btn.config(state=state_text)
        self.section_selector_cmb.config(state=state_text)
        self.structure_selector_cmb.config(state=state_text)
        self.wafer_size_selector_cmb.config(state=state_text)       
         
    def generation_safe_thread(self, filename):
        self.wafer.generate_setups(filename)
        self.set_status_bar("Done creating file!",2)
        self.disable_controls(False)

    def generate(self):
        filename = self.filename_ent.get()

        my_thread = thread.start_new_thread( self.generation_safe_thread, (filename,) )
        self.disable_controls(True)

        self.set_status_bar("Creating {0}.gds file ...".format(filename),-1)
        
    def generate_sections(self):
        number_rows = int(self.rows_ent.get())
        number_cols = int(self.cols_ent.get())
        
        self.wafer.partition(number_rows, number_cols)
        self.update_sections()
        
        self.set_status_bar("Maximum number of sections: {0}".format(number_rows*number_cols),2)
    def section_changed(self, event):

        
        section = int(self.selected_section.get())
        setup = None
        self.radius_ent.delete(0, tk.END)
        self.distance_ent.delete(0,tk.END)
            
        try:
            setup = self.wafer.setups[section]
            self.radius_ent.insert(0,str(setup['radius']))
            self.distance_ent.insert(0,str(setup['distance']))
            
            index = 0
            for structure in self.wafer.STRUCTURES:
                if structure == setup['structure']:
                    break;
                index += 1

            self.structure_selector_cmb.current(index)

        except Exception as e:
            self.structure_selector_cmb.current(0)
            self.radius_ent.insert(0,'0.0')
            self.distance_ent.insert(0,'0.0')
    
    def wafer_size_changed(self, event):
        size = int(self.selected_wafer.get())

        self.wafer.change_wafer_size(size)

    def save_section(self):
        section = int(self.selected_section.get())
        radius = float(self.radius_ent.get())
        distance = float(self.distance_ent.get())
        
        self.wafer.add_setup(distance,
                        radius, 
                        self.wafer.STRUCTURES[self.structure_selector_cmb.current()], 
                        section)
        self.set_status_bar("Section {0} saved!".format(section),2)

    def update_sections(self):
        self.section_selector_cmb['values'] = range(1, self.wafer.num_sections + 1)
    
    def check_only_int(self, event):
        if event.char in '1234567890\b\t':
            entry_text = event.widget.get()
            if len(entry_text) == 0:
                if event.char == '0':
                    return 'break'
            #print event.char
        elif event.keysym not in ('Alt_r', 'Alt_L', 'F4'):
            #print event.keysym
            return 'break'


    def check_only_float(self, event):
        if event.char in '1234567890.\b\t':
            entry_text = event.widget.get()
            if event.char == '.':
                if '.' in entry_text:
                    return 'break'
            if len(entry_text) == 1:
                if entry_text[0] == '0':
                    if event.char not in '.\b\t':
                        return 'break'
            #print event.char
        elif event.keysym not in ('Alt_r', 'Alt_L', 'F4'):
            #print event.keysym
            return 'break'

    def data_focus_out(self, event):
        text = event.widget.get()
        
        if text == '':
            event.widget.insert(0,'0.0')
    
    def row_col_focus_out(self, event):
        text = event.widget.get()
        
        if text == '':
            event.widget.insert(0,'1')
    
    def reset_status_bar(self,delay):
        if delay != -1:
            time.sleep(delay)
            self.status_lbl.config(text="...")

    def set_status_bar(self, message, delay):
        self.status_lbl.config(text=message)
        thread.start_new_thread( self.reset_status_bar, (delay,) )

    def initialize(self):
        #creating outer containers
        self.optionSection = tk.LabelFrame(self, text="Manage Sections")
        self.structureSection = tk.LabelFrame(self.optionSection, text="Options")
        self.sectionsLayoutSection = tk.LabelFrame(self.optionSection, text="Sections Layout")
        self.sub_structureSection = tk.LabelFrame(self.structureSection, text='Structure')
        self.statusSection = tk.LabelFrame(self)

        #creating labels
        #self.sections_gen_lbl = tk.Label(self.optionSection, text="Sections layout:")
        self.rows_lbl = tk.Label(self.sectionsLayoutSection, text="Rows:")
        self.cols_lbl = tk.Label(self.sectionsLayoutSection, text="Columns:")
        self.wafer_size_lbl = tk.Label(self.sectionsLayoutSection, text="Wafer Size(mm):")

        self.filename_lbl = tk.Label(self.optionSection, text="File name:")

        self.section_lbl = tk.Label(self.structureSection, text="Selected Section:")
        self.distance_lbl = tk.Label(self.structureSection, text="Distance between pilars(um):")
        self.radius_lbl = tk.Label(self.structureSection, text="Base radius(um):")
       
        self.status_lbl = tk.Label(self.statusSection, text="Ready!")

        #creating text fields
        self.rows_ent = tk.Entry(self.sectionsLayoutSection, width = 10)
        self.rows_ent.insert(0,'1')
        self.cols_ent = tk.Entry(self.sectionsLayoutSection, width = 10)
        self.cols_ent.insert(0,'1')
       
        self.filename_ent = tk.Entry(self.optionSection)

        self.distance_ent = tk.Entry(self.structureSection, width = 10)
        self.radius_ent = tk.Entry(self.structureSection, width = 10)
        
        #binding float and int  checking methods to the entries
        self.distance_ent.bind('<KeyPress>', self.check_only_float)
        self.radius_ent.bind('<KeyPress>', self.check_only_float)
        self.rows_ent.bind('<KeyPress>', self.check_only_int)
        self.cols_ent.bind('<KeyPress>', self.check_only_int)

        #binding focus management to components
        self.distance_ent.bind('<FocusOut>', self.data_focus_out)
        self.radius_ent.bind('<FocusOut>', self.data_focus_out)
        
        self.rows_ent.bind('<FocusOut>', self.row_col_focus_out)
        self.cols_ent.bind('<FocusOut>', self.row_col_focus_out)

        #creating buttons
        self.create_file_btn = tk.Button(self.optionSection, text="Create", command=self.generate)
        self.generate_sections_btn = tk.Button(self.sectionsLayoutSection, text="Generate", command=self.generate_sections)
        self.save_section_btn = tk.Button(self.structureSection, text="Save", command=self.save_section)

        #creating section selector
        self.selected_section = tk.StringVar()
        self.section_selector_cmb = ttk.Combobox(self.structureSection, width=5 ,textvariable=self.selected_section)
        self.section_selector_cmb.bind('<<ComboboxSelected>>', self.section_changed)
        
        self.selected_structure = tk.StringVar()
        self.structure_selector_cmb = ttk.Combobox(self.sub_structureSection, width=5 ,textvariable=self.selected_structure)
        self.structure_selector_cmb['values'] = self.wafer.STRUCTURES

        self.selected_wafer = tk.StringVar()
        self.wafer_size_selector_cmb = ttk.Combobox(self.sectionsLayoutSection, width=5, textvariable=self.selected_wafer)
        self.wafer_size_selector_cmb['values'] = self.wafer.SIZES
        self.wafer_size_selector_cmb.bind('<<ComboboxSelected>>', self.wafer_size_changed)

        #adding components to the window
        self.optionSection.pack(padx=5, pady=2)
        self.statusSection.pack(padx=5, pady=2, fill=tk.X)
    
        
        self.status_lbl.grid(row=0, column=0, padx=5, pady=5)

        #self.sections_gen_lbl.grid(row=0, column=0, pady=5)
        self.sectionsLayoutSection.grid(row=0, column=0, columnspan=4, padx=5, pady=5)
        self.cols_lbl.grid(row=0, column=0,padx=5, pady=5)
        self.cols_ent.grid(row=0, column=1,padx=5, pady=5)
        self.rows_lbl.grid(row=1, column=0,padx=5, pady=5)
        self.rows_ent.grid(row=1, column=1,padx=5, pady=5)
        self.generate_sections_btn.grid(row=2, column=0, padx=5, pady=5)

        self.wafer_size_lbl.grid(row=0, column=2, padx=5, pady=5)
        self.wafer_size_selector_cmb.grid(row=0, column=3, padx=5, pady=5)

        self.structureSection.grid(row=1, column=0, columnspan=4, padx=5, pady=5)
        self.sub_structureSection.grid(row=0, column=3, rowspan=1, padx=5, pady=5)
        self.structure_selector_cmb.grid(row=0, column=0, padx=5, pady=5)
        self.section_lbl.grid(row=0, column=0,padx=5, pady=5)
        self.section_selector_cmb.grid(row=0, column=1, padx=5, pady=5)
        self.distance_lbl.grid(row=1, column=0,padx=5, pady=5)
        self.distance_ent.grid(row=1, column=1,padx=5)
        self.radius_lbl.grid(row=2, column=0,padx=5, pady=5)
        self.radius_ent.grid(row=2, column=1,padx=5)

        self.save_section_btn.grid(row=4, column=0,padx=5, pady=5)
        
        self.filename_lbl.grid(row=5, column=0,padx=5, pady=5)

        self.filename_ent.grid(row=5, column=1,padx=5)

        self.create_file_btn.grid(row=5, column=2,padx=5, pady=5)

window = app_gui()
window.title("GDS Lithograpy mask generator")

window.mainloop()
