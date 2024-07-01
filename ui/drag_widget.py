from PyQt6.QtCore import QMimeData, Qt
from PyQt6.QtGui import QDrag, QPixmap
from PyQt6.QtWidgets import (
    QWidget, 
    QLabel, 
    QCheckBox, 
    QVBoxLayout, 
    QHBoxLayout, 
    QFrame,
    QCheckBox, 
    QLabel, 
    QRadioButton)

class DragWidget(QWidget):
    def __init__(self, parent=None, flags=Qt.WindowType.Widget):
        super().__init__(parent, flags)

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            # Render at x2 pixel ratio to avoid blur on Retina screens.
            pixmap = QPixmap(self.size().width() * 2, self.size().height() * 2)
            pixmap.setDevicePixelRatio(2)
            self.render(pixmap)
            drag.setPixmap(pixmap)

            drag.exec(Qt.DropAction.MoveAction)
            self.show() # Show this widget again, if it's dropped outside.

class DragLabel(QLabel, DragWidget):
    def __init__(self, person_id: int, person_name: str, parent=None):
        super().__init__(str(person_name), parent)  # Ensure text is a string
        self.person_id = person_id
        self.person_name = person_name
        # The size needs refactoring, so a drag label creates a target indicator that can be used for itself
        self.setContentsMargins(25, 5, 25, 5)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("border: 1px solid black;")
        # Store data separately from display label, but use label for default.
        self.data = (self.person_id, self.person_name)

    
    def set_data(self, data):
        self.data = data
    
    def get_person_id(self) -> int:
        return self.person_id
class DragSortWidget(DragWidget):
    def __init__(self, label_text, var_name, checkbox_state=False, radio_option="Spread", parent=None):
        super(DragSortWidget, self).__init__(parent)
        
        # Initialize widgets
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(checkbox_state)
        
        self.label = QLabel(label_text)
        self.var_name = var_name
        
        self.radio1 = QRadioButton("Spread")
        self.radio2 = QRadioButton("Focus")
        
        if radio_option == "Spread":
            self.radio1.setChecked(True)
        elif radio_option == "Focus":
            self.radio2.setChecked(True)
        
        # Create vertical separators
        self.separator1 = QFrame()
        self.separator1.setFrameShape(QFrame.Shape.VLine)
        self.separator1.setFrameShadow(QFrame.Shadow.Sunken)
        
        self.separator2 = QFrame()
        self.separator2.setFrameShape(QFrame.Shape.VLine)
        self.separator2.setFrameShadow(QFrame.Shadow.Sunken)
        
        # Layouts
        main_layout = QHBoxLayout()
        
        main_layout.addWidget(self.checkbox)
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.separator1)
        main_layout.addWidget(self.radio1)
        main_layout.addWidget(self.separator2)
        main_layout.addWidget(self.radio2)
        
        self.setLayout(main_layout)
    
    def is_checked(self) -> bool:
        return self.checkbox.isChecked()
    
    def get_label_text(self):
        return self.label.text()
    
    def get_selected_radio(self):
        if self.radio1.isChecked():
            return "Spread"
        elif self.radio2.isChecked():
            return "Focus"
        else:
            return None
        
    def get_data(self):
        return {
            'label_text': self.get_label_text(),
            'var_name': self.var_name,
            'is_checked': self.is_checked(),
            'selected_radio': self.get_selected_radio()
        }        

    def set_values(self, checkbox_state: bool, radio_option: str):
        self.checkbox.setChecked(checkbox_state) 
        if radio_option == "Spread":
            self.radio1.setChecked(True)
        elif radio_option == "Focus":
            self.radio2.setChecked(True)
class DragTargetIndicator(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(25, 5, 25, 5)
        self.setStyleSheet(
            "QLabel { background-color: #ccc; border: 1px solid black; }"
        )