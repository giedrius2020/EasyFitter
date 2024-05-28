from PyQt5.QtWidgets import QSlider, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal

from PyQt5.QtWidgets import QSlider, QLabel
from PyQt5.QtCore import pyqtSignal, Qt
import math

class FloatSlider(QSlider):
    valueChangedFloat = pyqtSignal(str)

    def __init__(self, orientation, parent=None):
        super(FloatSlider, self).__init__(orientation, parent)
        self._min = 0.0
        self._max = 1.0
        # self._step = 0.001
        self._label = QLabel(self)
        self._label.setAlignment(Qt.AlignCenter)
        self._label.setGeometry(0, 0, 40, 20)

    def setMinimum(self, value):
        self._min = value

    def setMaximum(self, value):
        self._max = value

    def value(self):
        return self._min + (self._max - self._min) * super(FloatSlider, self).value() / self.maximum()

    def setValue(self, value):
        scaled_value = round((value - self._min) / (self._max - self._min) * self.maximum())
        super(FloatSlider, self).setValue(scaled_value)
        self.valueChangedFloat.emit(str(value))
        self.updateLabel()

    def updateLabel(self):
        value = self.value()
        exponent = int(math.floor(math.log10(abs(value))))
        mantissa = value / (10 ** exponent)
        rounded_mantissa = round(mantissa, 2)
        formatted_value = "{:.3f}e{}".format(rounded_mantissa, exponent)
        self._label.setText(str(formatted_value))
        self._label.adjustSize()
        self._label.move((self.width() - self._label.width()) / 2, -self._label.height())
        # print("test: ", formatted_value)

        return formatted_value

    def resizeEvent(self, event):
        super(FloatSlider, self).resizeEvent(event)
        self.updateLabel()

    def sliderChange(self, change):
        if change == QSlider.SliderValueChange:
            formatted_val = self.updateLabel()
            self.valueChangedFloat.emit(formatted_val)
        super(FloatSlider, self).sliderChange(change)


class SliderWidget:
    def __init__(self):
        self.slider_labels = []

    def create_slider(self, layout, name, min_val, max_val, default_val):
        slider_layout = QHBoxLayout()
        label = QLabel(name)
        slider = FloatSlider(Qt.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(default_val)
        slider_layout.addWidget(label)
        slider_layout.addWidget(slider)

        # # Displaying slider value next to it:
        # value_label = QLabel(str(default_val))
        # slider.valueChangedFloat.connect(lambda value, label=value_label: label.setText(value))
        # slider_layout.addWidget(value_label)

        # QLineEdit for entering value by hand
        value_edit = QLineEdit(str(default_val))
        value_edit.setFixedWidth(100)
        slider_layout.addWidget(value_edit)
        value_edit.setStyleSheet("background-color: #6de3c2;")


        # Function to update slider and value label when QLineEdit value changes
        def update_from_edit():
            new_value = float(value_edit.text())
            value_edit.setText("{:.2e}".format(new_value))
            slider.setValue(new_value)

        # Function to update QLineEdit when slider value changes
        def update_from_slider(value):
            value_edit.setText(str(value))

        slider.valueChangedFloat.connect(update_from_slider)
        value_edit.editingFinished.connect(update_from_edit)

        # LineEdits for editing min, max, and step
        min_edit = QLineEdit("{:.1e}".format(min_val))
        max_edit = QLineEdit("{:.1e}".format(max_val))
        min_edit.setFixedWidth(100)
        max_edit.setFixedWidth(100)
        # Set background color using style sheets
        min_edit.setStyleSheet("background-color: #9cadb8;")
        # Set background color using style sheets
        max_edit.setStyleSheet("background-color: #9cadb8;")

        slider_layout.addWidget(min_edit)
        slider_layout.addWidget(max_edit)

        # Apply button to update min, max, and step values
        apply_button = QPushButton("Apply new limits")
        apply_button.setEnabled(False)  # Initially disabled
        slider_layout.addWidget(apply_button)

        # Function to enable/disable Apply button based on input changes
        def enable_apply():
            apply_button.setEnabled(min_edit.isModified() or max_edit.isModified())

        # Connect signals from line edits to enable_apply function
        min_edit.textChanged.connect(enable_apply)
        max_edit.textChanged.connect(enable_apply)

        # Apply changes function
        def apply_changes():
            min_val = float(min_edit.text())
            max_val = float(max_edit.text())

            slider.setMinimum(min_val)
            slider.setMaximum(max_val)

            # Update the current value label
            # current_value = slider.value()

            # Reset modified state
            min_edit.setModified(False)
            max_edit.setModified(False)
            apply_button.setEnabled(False)  # Disable after applying changes

        apply_button.clicked.connect(apply_changes)

        layout.addLayout(slider_layout)
        self.slider_labels.append(label)
        return slider


