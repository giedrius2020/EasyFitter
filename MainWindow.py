import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QPushButton, \
    QCheckBox
from PyQt5.QtCore import Qt
from TableWindow import TableWindow
from SliderWidget import SliderWidget
import pandas as pd

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("EasyFitter")



        self.table_window = TableWindow()

        # Connect the signal from TableWindow to a slot in MainWindow
        self.table_window.collect_data_signal.connect(self.update_graph_with_new_data)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Add checkbox to switch between functions
        self.vol_checkbox = QCheckBox("Show Volume component", self)
        self.vol_checkbox.setChecked(True)
        self.layout.addWidget(self.vol_checkbox)
        self.vol_checkbox.stateChanged.connect(self.update_plot)

        # Add checkbox to switch between functions
        self.surf_checkbox = QCheckBox("Show Surface component", self)
        self.surf_checkbox.setChecked(True)
        self.layout.addWidget(self.surf_checkbox)
        self.surf_checkbox.stateChanged.connect(self.update_plot)

        # Labels to show slider values
        self.slider_labels = []


        # Initialize sliders
        self.slider_widget = SliderWidget()

        a = 3.3e-3  # I1
        b = 1.2e-5  # tau1
        c = 0.2     # beta
        d = 3.3e-3  # I2
        e = 1.2e-6        # tau2
        f = 3.3e-3
        g = 1.2e-8

        self.a_slider = self.slider_widget.create_slider(self.layout,
                                                         "I1",
                                                         min_val=a/10,
                                                         max_val=a*3,
                                                         default_val=a)
        self.b_slider = self.slider_widget.create_slider(self.layout,
                                                         name="tau1",
                                                         min_val=b/100,
                                                         max_val=b*100,
                                                         default_val=b)
        self.c_slider = self.slider_widget.create_slider(self.layout,
                                                         name="beta",
                                                         min_val=c/10,
                                                         max_val=c*10,
                                                         default_val=c)
        self.d_slider = self.slider_widget.create_slider(self.layout,
                                                         name="I2",
                                                         min_val=d / 10,
                                                         max_val=d * 3,
                                                         default_val=d)
        self.e_slider = self.slider_widget.create_slider(self.layout,
                                                         name="tau2",
                                                         min_val=e / 100,
                                                         max_val=e * 1000,
                                                         default_val=e)
        self.f_slider = self.slider_widget.create_slider(self.layout,
                                                         name="i3",
                                                         min_val=f / 100,
                                                         max_val=f * 100,
                                                         default_val=f)

        self.g_slider = self.slider_widget.create_slider(self.layout,
                                                         name="tau3",
                                                         min_val=g / 100,
                                                         max_val=g * 1,
                                                         default_val=g)

        # Initialize plot1
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')  # Set background color to white
        self.layout.addWidget(self.plot_widget)
        self.plot_widget.getPlotItem().setLogMode(x=True, y=False)  # Set x-axis to log10

        # Initialize plot2
        self.plot_widget_2 = pg.PlotWidget()
        self.plot_widget_2.setBackground('w')  # Set background color to white
        self.layout.addWidget(self.plot_widget_2)
        self.plot_widget_2.getPlotItem().setLogMode(x=True, y=False)  # Set x-axis to log10

        # Connect slider signals to update_plot function
        self.a_slider.valueChanged.connect(self.update_plot)
        self.b_slider.valueChanged.connect(self.update_plot)
        self.c_slider.valueChanged.connect(self.update_plot)
        self.d_slider.valueChanged.connect(self.update_plot)
        self.e_slider.valueChanged.connect(self.update_plot)
        self.f_slider.valueChanged.connect(self.update_plot)
        self.g_slider.valueChanged.connect(self.update_plot)

        self.show_table_button = QPushButton("Show Table Window")
        self.show_table_button.clicked.connect(self.show_table_window)
        self.layout.addWidget(self.show_table_button)


        self.scatter_datasets = self.generate_scatter_data_from_df(self.table_window.datasets)
        self.update_plot()

    def update_graph_with_new_data(self):
        self.update_plot()
        self.scatter_datasets = self.generate_scatter_data_from_df(self.table_window.datasets)
        for ds in self.table_window.datasets:
            print(ds.tab_name, ":\n", ds.df)

    def show_table_window(self):
        self.table_window.show()

    def update_plot(self):
        a = self.a_slider.value()
        b = self.b_slider.value()
        c = self.c_slider.value()
        d = self.d_slider.value()
        e = self.e_slider.value()
        f = self.f_slider.value()
        g = self.g_slider.value()

        # Clear both plot widgets
        self.plot_widget.clear()
        self.plot_widget_2.clear()

        for ds in self.table_window.datasets:
            # Plot data on the first plot widget
            data_line = pg.PlotDataItem(x=ds.df['x'], y=ds.df['y'], pen=pg.mkPen(color='blue', width=1), name="Data")
            self.plot_widget.addItem(data_line)

            # Plot fitting line on the first plot widget
            y_line = self.generate_y_for_fit_function(ds.df['x'], a, b, c, d, e, f, g)
            line = pg.PlotDataItem(x=ds.df['x'], y=y_line, pen=pg.mkPen(color='red', width=2), name="Fit")
            self.plot_widget.addItem(line)

            # # Plot data on the second plot widget
            # data_line_2 = pg.PlotDataItem(x=ds.df['x'], y=ds.df['y'], pen=pg.mkPen(color='green', width=1))
            # self.plot_widget_2.addItem(data_line_2)

            # Plot fitting line on the second plot widget (using a different function)
            x_line_2, y_line_2 = self.generate_kupra_data_graph(ds.df['x'], ds.df['y'], a)  # Adjust this function accordingly
            line_2 = pg.PlotDataItem(x=ds.df['x'], y=y_line_2, pen=pg.mkPen(color='blue', width=2), name="Data")
            self.plot_widget_2.addItem(line_2)

            # Plot fitting line on the second plot widget (using a different function)
            x_line_2, y_line_2 = self.generate_kupra_data_graph(ds.df['x'], y_line, a)  # Adjust this function accordingly
            line_2 = pg.PlotDataItem(x=ds.df['x'], y=y_line_2, pen=pg.mkPen(color='red', width=2), name="Fit")
            self.plot_widget_2.addItem(line_2)


        # Add legend to the plot widgets after adding all items
        self.plot_widget.addLegend()
        self.plot_widget_2.addLegend()


    def generate_y_for_fit_function(self, x, a, b, c, d, e, f, g):
        # TODO: edit function based on your needs.
        ser_component = a*np.exp(-(x/b)**c)
        y = ser_component

        if self.vol_checkbox.isChecked():
            volume_component = d*np.exp(-(x/e))
            y = y + volume_component
        if self.surf_checkbox.isChecked():
            surface_component = f*np.exp(-(x/g))
            y = y + surface_component
        return y

    def generate_kupra_data_graph(self, x, y, a):
        # TODO: edit function based on your needs.
        x_transformed = np.log10(x)
        y_transformed = np.log10(-np.log10(y / a))

        return x_transformed, y_transformed

    def generate_scatter_data_from_df(self, datasets):
        value_sets = []
        for ds in datasets:
            x = ds.df["x"].values
            y = ds.df["y"].values
            value_sets.append((x, y))
        return value_sets




