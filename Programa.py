import tkinter as tk
from tkinter import filedialog, colorchooser
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FuncFormatter, FixedLocator

class OscilloscopeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI Osciloscopio")

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.load_button = tk.Button(self.frame, text="Cargar CSV", command=self.load_csv, font=("Helvetica", 14))
        self.load_button.pack(side=tk.LEFT)

        self.grid_button = tk.Button(self.frame, text="Mostrar Grilla", command=self.toggle_grid, font=("Helvetica", 14))
        self.grid_button.pack(side=tk.LEFT)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.controls_frame = tk.Frame(root)
        self.controls_frame.pack()

        self.scale_vars = {}
        self.offset_vars = {}

        self.colors = {}
        self.channel_buttons = {}
        self.current_data = None
        self.grid_enabled = True  # Estado inicial de las grillas

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            data = pd.read_csv(file_path)
            self.create_controls(data)
            self.plot_data(data)

    def toggle_grid(self):
        self.grid_enabled = not self.grid_enabled
        self.plot_data(self.current_data)  # Vuelve a trazar para actualizar las grillas

    def create_controls(self, data):
        for widget in self.controls_frame.winfo_children():
            if isinstance(widget, tk.Entry) or isinstance(widget, tk.Label):
                widget.pack_forget()

        canales = data.columns[1:]
        self.scale_vars.clear()
        self.offset_vars.clear()

        for canal in canales:
            self.scale_vars[canal] = tk.DoubleVar(value=1.0)
            self.offset_vars[canal] = tk.DoubleVar(value=0.0)

            scale_label = tk.Label(self.controls_frame, text=f"Escala {canal}")
            scale_label.pack(side=tk.LEFT)
            scale_entry = tk.Entry(self.controls_frame, textvariable=self.scale_vars[canal])
            scale_entry.pack(side=tk.LEFT)

            offset_label = tk.Label(self.controls_frame, text=f"Desplazar {canal}")
            offset_label.pack(side=tk.LEFT)
            offset_entry = tk.Entry(self.controls_frame, textvariable=self.offset_vars[canal])
            offset_entry.pack(side=tk.LEFT)

            button = tk.Button(self.controls_frame, text=f"Seleccionar color para {canal}", command=lambda ch=canal: self.select_color(ch), font=("Helvetica", 14))
            button.pack(side=tk.LEFT)
            self.channel_buttons[canal] = button

    def select_color(self, canal):
        color_code = colorchooser.askcolor(title=f"Elegir color del canal {canal}")[1]
        if color_code:
            self.colors[canal] = color_code
            if self.current_data is not None:
                self.plot_data(self.current_data)

    def plot_data(self, data):
        self.current_data = data
        self.ax.clear()
        num_columns = len(data.columns)

        if num_columns < 2:
            print("No hay suficientes Columnas")
            return

        tiempo = data.columns[0]
        canales = data.columns[1:]

        for canal in canales:
            scale = self.scale_vars[canal].get()
            offset = self.offset_vars[canal].get()
            color = self.colors.get(canal, 'blue')
            self.ax.plot(data[tiempo], data[canal] * scale + offset, label=canal, color=color)

        # Determine the time range to set appropriate scale
        tiempo_max = data[tiempo].max()
        if tiempo_max < 1e-3:
            scale = 1e6  # Microsegundo
            unit = "(µs)"
        elif tiempo_max < 1:
            scale = 1e3  # Milisegundo
            unit = "(ms)"
        else:
            scale = 1  # Segundo
            unit = "(s)"

        def time_formatter(x, pos):
            return f'{x * scale:.2f}'

        self.ax.xaxis.set_major_formatter(FuncFormatter(time_formatter))

        self.ax.set_xlabel("Tiempo "+unit)
        self.ax.set_ylabel("Amplitud")
        self.ax.legend()
        # Configuración de las grillas
        if self.grid_enabled:
            self.ax.grid(True)
        else:
            self.ax.grid(False)

        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = OscilloscopeApp(root)
    root.mainloop()
