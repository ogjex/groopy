import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog
from PyQt6.QtGui import QColor
from ButtonPresenter import Presenter
import csv
from typing import Protocol

class Presenter(Protocol):
    def handle_save_colors(self) -> None:
        ...
    def handle_open_csv_file(self, filename):
        ...
    def handle_save_csv_file(self, filename):
        ...

class ColorButtonWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.colors = ["blue", "green", "red", "yellow"]
        self.current_color_index = 0  # Index of the current color

    def initUI(self, presenter:Presenter):
        # Create layout for colored buttons
        hbox_layout = QHBoxLayout()
        self.buttons = []
        self.presenter = presenter

        for i in range(4):
            button = QPushButton(self)
            button.setFixedSize(50, 50)  # Set fixed size for buttons
            hbox_layout.addWidget(button)
            self.buttons.append(button)

            # Connect button click signal to color change function
            button.clicked.connect(self.changeButtonColor)

        # Create layout for save and get color buttons
        vbox_layout = QVBoxLayout()

        # Add colored buttons to layout
        vbox_layout.addLayout(hbox_layout)

        # Add "Open CSV" button
        open_button = QPushButton("Open CSV", self)
        open_button.clicked.connect(self.openCSV)
        vbox_layout.addWidget(open_button)

        # Add "Save" button
        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.saveCSV)
        vbox_layout.addWidget(save_button)

        self.setLayout(vbox_layout)

        # Set initial colors
        self.setButtonColors()

    def changeButtonColor(self):
        # Change the color of the clicked button
        sender = self.sender()
        index = self.buttons.index(sender)
        self.current_color_index = (self.current_color_index + 1) % len(self.colors)
        color = self.colors[self.current_color_index]
        sender.setStyleSheet("background-color: {}".format(color))

    def loadButtonColors(self, color_list):
        for button, color in zip(self.buttons, color_list):
            self.setButtonColor(button, color)

    def setButtonColors(self):
        for button, color in zip(self.buttons, self.colors):
            self.setButtonColor(button, color)

    def setButtonColor(self, button, color):
        button.setStyleSheet("background-color: {}".format(color))    

    def getColors(self):
        # Get and return the color values of the buttons
        return [button.palette().button().color().name() for button in self.buttons]

    def saveCSV(self):
        # Open file dialog to select a CSV file
        
        fileName, _ = QFileDialog.getSaveFileName(self,"Save CSV File", "","CSV Files (*.csv)")
        if fileName:
            button_color_list = self.getColors()
            self.presenter.handle_save_csv_file(fileName, button_color_list)

    def openCSV(self):
        # Open file dialog to select a CSV file
        
        fileName, _ = QFileDialog.getOpenFileName(self,"Open CSV File", "","CSV Files (*.csv)")
        if fileName:
            self.presenter.handle_open_csv_file(fileName)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
