import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QColorDialog, QDoubleSpinBox, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QFormLayout, QSplitter
from PyQt5.QtCore import Qt  # Importar Qt desde PyQt5.QtCore
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import FuncFormatter

class OscilloscopeApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(OscilloscopeApp, self).__init__()
        uic.loadUi("interfaz.ui", self)
        self.setWindowTitle("GUI Osciloscopio")

        # Crear un widget principal y un layout vertical
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        # Crear un layout horizontal para los botones
        button_layout = QHBoxLayout()

        # Crear los botones y añadirlos al layout de botones
        self.load_button = QPushButton("Cargar CSV")
        self.grid_button = QPushButton("Grilla")
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.grid_button)

        # Añadir el layout de botones al layout principal
        main_layout.addLayout(button_layout)

        # Crear un splitter vertical para el gráfico y los controles
        self.splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(self.splitter)

        # Widget para el gráfico
        self.plot_widget = QWidget()
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        plot_layout = QVBoxLayout(self.plot_widget)
        plot_layout.addWidget(self.canvas)

        # Añadir el widget de gráfico al splitter
        self.splitter.addWidget(self.plot_widget)

        # Widget para los controles
        self.controls_widget = QWidget()
        self.controls_layout = QVBoxLayout(self.controls_widget)
        self.controls_layout.setContentsMargins(5, 5, 5, 5)  # Margenes pequeños
        self.controls_layout.setSpacing(5)  # Espaciado pequeño
        self.controls_tabWidget = QtWidgets.QTabWidget()
        self.controls_layout.addWidget(self.controls_tabWidget)

        # Añadir el widget de controles al splitter
        self.splitter.addWidget(self.controls_widget)

        # Configurar el tamaño inicial de las secciones del splitter
        self.splitter.setSizes([800, 200])  # Más espacio para el gráfico

        # Conectar los botones a sus funciones
        self.load_button.clicked.connect(self.load_csv)
        self.grid_button.clicked.connect(self.toggle_grid)

        self.scale_vars = {}
        self.offset_vars = {}
        self.colors = {}
        self.channel_tabs = {}
        self.current_data = None
        self.grid_enabled = True
        # Habilitar la funcionalidad de arrastrar y soltar
        self.setAcceptDrops(True)
    # Agregar las siguientes funciones a la clase OscilloscopeApp
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.endswith('.csv'):
                data = pd.read_csv(file_path)
                self.create_controls(data)
                self.plot_data(data)
                break

    def create_controls(self, data):
        for i in reversed(range(self.controls_tabWidget.count())):
            widget = self.controls_tabWidget.widget(i)
            self.controls_tabWidget.removeTab(i)
            widget.deleteLater()

        canales = data.columns[1:]
        self.scale_vars.clear()
        self.offset_vars.clear()

        for canal in canales:
            tab_widget = QWidget()
            tab_layout = QFormLayout(tab_widget)

            scale_label = QLabel(f"Escala")
            scale_var = QDoubleSpinBox(value=1.0, minimum=-float('inf'))
            scale_var.valueChanged.connect(self.update_plot)
            self.scale_vars[canal] = scale_var
            tab_layout.addRow(scale_label, scale_var)

            offset_label = QLabel(f"Desplazamiento")
            offset_var = QDoubleSpinBox(value=0.0, minimum=-float('inf'))
            offset_var.valueChanged.connect(self.update_plot)
            self.offset_vars[canal] = offset_var
            tab_layout.addRow(offset_label, offset_var)

            button = QPushButton(f"Color para {canal}")
            button.clicked.connect(lambda _, ch=canal: self.select_color(ch))
            tab_layout.addRow(button)

            self.controls_tabWidget.addTab(tab_widget, canal)
            self.channel_tabs[canal] = tab_widget

    def update_plot(self):
        if self.current_data is not None:
            self.plot_data(self.current_data)

    def load_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Cargar CSV", "", "CSV files (*.csv)")
        if file_path:
            data = pd.read_csv(file_path)
            self.create_controls(data)
            self.plot_data(data)

    def toggle_grid(self):
        if self.current_data is not None:
            self.grid_enabled = not self.grid_enabled
            self.plot_data(self.current_data)

    def select_color(self, canal):
        color = QColorDialog.getColor()
        if color.isValid():
            self.colors[canal] = color.name()
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
            scale = self.scale_vars[canal].value()
            offset = self.offset_vars[canal].value()
            color = self.colors.get(canal, 'blue')
            self.ax.plot(data[tiempo], data[canal] * scale + offset, label=canal, color=color)

        tiempo_max = data[tiempo].max()
        if tiempo_max < 1e-3:
            scale = 1e6
            unit = "(µs)"
        elif tiempo_max < 1:
            scale = 1e3
            unit = "(ms)"
        else:
            scale = 1
            unit = "(s)"

        def time_formatter(x, pos):
            return f'{x * scale:.2f}'

        self.ax.xaxis.set_major_formatter(FuncFormatter(time_formatter))

        self.ax.set_xlabel("Tiempo " + unit)
        self.ax.set_ylabel("Amplitud")
        self.ax.legend()
        self.ax.grid(self.grid_enabled)

        self.canvas.draw()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    osc_app = OscilloscopeApp()
    osc_app.show()
    sys.exit(app.exec_())
