import tkinter as tk
import generator as generator
import ttk

class app_gui(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.initialize()

    def generate(self):
        filename    = self.filename_ent.get()
        distance    = int(self.distance_ent.get())
        radius      = int(self.radius_ent.get())
        overhang    = int(self.overhang_ent.get())
        number_rows = int(self.rows_ent.get())
        number_cols = int(self.cols_ent.get())
        
        generator.generate_dsg_file(filename, 
                distance, 
                radius,
                overhang,
                number_rows,
                number_cols)

    def initialize(self):
        #creating outer containers
        self.tabSection = ttk.Notebook(self)
        self.previewSection = tk.LabelFrame(self, text="Preview")

        #creating tabs
        self.round_pilars_tab = ttk.Frame(self.tabSection)
        self.grid_tab = ttk.Frame(self.tabSection)
        
        #adding Tabs
        self.tabSection.add(self.round_pilars_tab, text="Pilars")
        self.tabSection.add(self.grid_tab, text="Grid")

        #preview canvas
        self.preview = tk.Canvas(self.previewSection)

        #creating labels
        self.filename_lbl = tk.Label(self.round_pilars_tab, text="Name of the file")
        self.distance_lbl = tk.Label(self.round_pilars_tab, text="Distance between pilars(um):")
        self.radius_lbl = tk.Label(self.round_pilars_tab, text="Base radius(um):")
        self.overhang_lbl = tk.Label(self.round_pilars_tab, text="Overhang size (um)")
        self.rows_lbl = tk.Label(self.round_pilars_tab, text="Number of rows:")
        self.cols_lbl = tk.Label(self.round_pilars_tab, text="Number of columns:")
        
        #creating text fields
        self.filename_ent = tk.Entry(self.round_pilars_tab)
        self.distance_ent = tk.Entry(self.round_pilars_tab)
        self.radius_ent = tk.Entry(self.round_pilars_tab)
        self.overhang_ent = tk.Entry(self.round_pilars_tab)
        self.rows_ent = tk.Entry(self.round_pilars_tab)
        self.cols_ent = tk.Entry(self.round_pilars_tab)
    
        #creating buttons
        self.generate_btn = tk.Button(self.round_pilars_tab, text="Generate", command=self.generate)

        #adding components to the window
        self.filename_lbl.pack(padx=5, pady=5)
        self.filename_ent.pack(padx=5)
        self.distance_lbl.pack(padx=5, pady=5)
        self.distance_ent.pack(padx=5)
        self.radius_lbl.pack(padx=5, pady=5)
        self.radius_ent.pack(padx=5)
        self.overhang_lbl.pack(padx=5, pady=5)
        self.overhang_ent.pack(padx=5)
        self.rows_lbl.pack(padx=5, pady=5)
        self.rows_ent.pack(padx=5)
        self.cols_lbl.pack(padx=5, pady=5)
        self.cols_ent.pack(padx=5)

        #self.tabSection.pack(expand=1, fill="both", side=tk.RIGHT)
        self.tabSection.pack(side=tk.RIGHT, fill= tk.Y, padx=5, pady=5)
        self.previewSection.pack(side=tk.LEFT,fill="both", expand=1, padx=5, pady=5)
        
        self.preview.pack(fill="both", expand=1)
        self.generate_btn.pack(padx=5, pady=5)


window = app_gui()
window.title("GDS Lithograpy mask generator")

window.geometry("{0}x{1}+0+0".format(int(window.winfo_screenwidth()*0.75),int(window.winfo_screenheight()*0.5)))

window.mainloop()
