import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QColorDialog, QDoubleSpinBox, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QFormLayout, QSplitter, QComboBox
from PyQt5.QtCore import Qt
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
import mplcursors

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
        self.logx_button = QComboBox()
        self.logx_button.addItems(["Escala X Lineal", "Escala X Logarítmica"])
        self.logy_button = QComboBox()
        self.logy_button.addItems(["Escala Y Lineal", "Escala Y Logarítmica"])
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.grid_button)
        button_layout.addWidget(self.logx_button)
        button_layout.addWidget(self.logy_button)

        # Añadir el layout de botones al layout principal
        main_layout.addLayout(button_layout)

        # Crear un splitter vertical para el gráfico y los controles
        self.splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(self.splitter)

        # Widget para el gráfico
        self.plot_widget = QWidget()
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)  # Crear la barra de herramientas
        plot_layout = QVBoxLayout(self.plot_widget)
        plot_layout.addWidget(self.canvas)
        plot_layout.addWidget(self.toolbar)  # Añadir la barra de herramientas al layout

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
        self.load_button.clicked.connect(self.LoadCsv)
        self.grid_button.clicked.connect(self.ToggleGrid)
        self.logx_button.currentIndexChanged.connect(self.UpdatePlot)
        self.logy_button.currentIndexChanged.connect(self.UpdatePlot)

        self.scale_vars = {}
        self.offset_vars = {}
        self.colors = {}
        self.channel_tabs = {}
        self.max_labels = {}  # Inicializar max_labels
        self.min_labels = {}  # Inicializar min_labels
        self.current_data = None
        self.grid_enabled = True
        self.cursors = []  # Inicializar los cursores
        # Habilitar la funcionalidad de arrastrar y soltar
        self.setAcceptDrops(True)
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.endswith('.csv'):
                data = pd.read_csv(file_path, header=[0, 1])
                data.columns = [' '.join(col).strip() for col in data.columns.values]  # Combinar las dos filas de encabezado
                self.CreateControls(data)
                self.PlotData(data)
                break

    def CreateControls(self, data):
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

            # Layout horizontal para centrar las etiquetas de máximo y mínimo
            min_max_layout = QHBoxLayout()
            min_max_layout.setAlignment(Qt.AlignCenter)

            max_label = QLabel(f"Máximo: N/A")
            self.max_labels[canal] = max_label
            min_max_layout.addWidget(max_label)

            min_label = QLabel(f"Mínimo: N/A")
            self.min_labels[canal] = min_label
            min_max_layout.addWidget(min_label)

            tab_layout.addRow(min_max_layout)

            scale_label = QLabel(f"Escala")
            scale_var = QDoubleSpinBox(value=1.0, minimum=-float('inf'))
            scale_var.valueChanged.connect(self.UpdatePlot)
            self.scale_vars[canal] = scale_var
            tab_layout.addRow(scale_label, scale_var)

            offset_label = QLabel(f"Desplazamiento")
            offset_var = QDoubleSpinBox(value=0.0, minimum=-float('inf'))
            offset_var.valueChanged.connect(self.UpdatePlot)
            self.offset_vars[canal] = offset_var
            tab_layout.addRow(offset_label, offset_var)

            button = QPushButton(f"Color para {canal}")
            button.clicked.connect(lambda _, ch=canal: self.SelectColor(ch))
            tab_layout.addRow(button)

            self.controls_tabWidget.addTab(tab_widget, canal)
            self.channel_tabs[canal] = tab_widget

    def UpdatePlot(self):
        if self.current_data is not None:
            self.PlotData(self.current_data)

    def LoadCsv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Cargar CSV", "", "CSV files (*.csv)")
        if file_path:
            data = pd.read_csv(file_path, header=[0, 1])
            data.columns = [' '.join(col).strip() for col in data.columns.values]  # Combinar las dos filas de encabezado
            self.CreateControls(data)
            self.PlotData(data)
    
    def ToggleGrid(self):
        if self.current_data is not None:
            self.grid_enabled = not self.grid_enabled
            self.PlotData(self.current_data)

    def SelectColor(self, canal):
        color = QColorDialog.getColor()
        if color.isValid():
            self.colors[canal] = color.name()
            if self.current_data is not None:
                self.PlotData(self.current_data)

    def PlotData(self, data):
        self.current_data = data
        self.ax.clear()
        num_columns = len(data.columns)

        if num_columns < 2:
            print("No hay suficientes Columnas")
            return

        tiempo = data.columns[0]
        canales = data.columns[1:]
        tiempo_max = data[tiempo].max()
        if tiempo_max < 1e-3:
            scale_t = 1e6
            unit = "(µs)"
        elif tiempo_max < 1:
            scale_t = 1e3
            unit = "(ms)"
        else:
            scale_t = 1
            unit = "(s)"

        for canal in canales:
            scale = self.scale_vars[canal].value()
            offset = self.offset_vars[canal].value()
            color = self.colors.get(canal, 'blue')
            self.ax.plot(data[tiempo]*scale_t, data[canal] * scale + offset, label=canal, color=color)

            max_idx = data[canal].idxmax()
            min_idx = data[canal].idxmin()

            max_time = data.loc[max_idx, tiempo] * scale_t
            max_value = data.loc[max_idx, canal] * scale + offset
            min_time = data.loc[min_idx, tiempo] * scale_t
            min_value = data.loc[min_idx, canal] * scale + offset

            self.ax.plot(max_time, max_value, 'ro')  # Punto máximo
            self.ax.plot(min_time, min_value, 'go')  # Punto mínimo

            self.max_labels[canal].setText(f"Máximo: {max_value:.2f} en {max_time:.2f} {unit}")
            self.min_labels[canal].setText(f"Mínimo: {min_value:.2f} en {min_time:.2f} {unit}")

        if self.logx_button.currentIndex() == 1:
            self.ax.set_xscale('log')
        else:
            self.ax.set_xscale('linear')

        if self.logy_button.currentIndex() == 1:
            self.ax.set_yscale('log')
        else:
            self.ax.set_yscale('linear')

        if self.grid_enabled:
            self.ax.grid(True)
        else:
            self.ax.grid(False)

        # Eliminar los cursores antiguos
        for cursor in self.cursors:
            cursor.remove()
        self.cursors.clear()

        # Crear nuevos cursores
        cursor = mplcursors.cursor(self.ax, hover=True)
        self.cursors.append(cursor)
        self.ax.set_xlabel("Tiempo " + unit)
        self.ax.set_ylabel("Amplitud")
        self.ax.legend()
        self.ax.legend()
        self.canvas.draw()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = OscilloscopeApp()
    window.show()
    app.exec_()
