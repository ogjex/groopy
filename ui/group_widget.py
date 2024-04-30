import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QLabel, QFrame, QGridLayout, QMainWindow
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal, QPoint
from PyQt5.QtGui import QDrag, QCursor

class DraggableLabel(QLabel):
    dragged = pyqtSignal(str)
    dropped = pyqtSignal(QPoint)

    def __init__(self, text):
        super().__init__(text)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.text())
            drag.setMimeData(mime_data)
            drag.exec_(Qt.MoveAction)
            self.dragged.emit(self.text())  # Emit signal indicating item is being dragged

    def dropEvent(self, event):
        drop_position = event.pos()
        self.dropped.emit(drop_position)  # Emit signal with drop position

class DragDropController:
    def __init__(self, app_window, group_widgets):
        self.app_window = app_window
        self.group_widgets = group_widgets

        for group_widget in self.group_widgets:
            for index in range(group_widget.participants_layout.count()):
                label = group_widget.participants_layout.itemAt(index).widget()
                label.dropped.connect(self.handleLabelDropped)

    def handleLabelDropped(self, drop_position):
        app_position = self.app_window.mapFromGlobal(QCursor.pos())
        print("Mouse position relative to application:", app_position)
        print("Drop position relative to widget:", drop_position)

        sender_label = self.sender()  # Get the label that emitted the dropped signal
        if sender_label:
            sender_label.setParent(None)  # Remove the label from its parent widget
class GroupWidget(QWidget):
    def __init__(self, title, participants, parent=None):
        super().__init__(parent)
        
        self.title = title
        self.participants = participants
        self.expanded = True
        
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        # Create a title label
        self.title_label = QLabel(self.title)
        layout.addWidget(self.title_label)
        
        # Create a frame for participants
        self.participants_frame = QFrame()
        self.participants_frame.setFrameShape(QFrame.StyledPanel)
        self.participants_layout = QVBoxLayout(self.participants_frame)
        layout.addWidget(self.participants_frame)
        
        self.setLayout(layout)
        
        # Hide participants initially
        self.participants_frame.show()
        
        # Populate participants
        self.populateParticipants()
        
        # Enable drag and drop
        self.setAcceptDrops(True)
        
    def populateParticipants(self):
        for participant in self.participants:
            label = DraggableLabel(participant)
            label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
            label.setMargin(2)
            label.setAlignment(Qt.AlignCenter)
            label.setFixedSize(100, 20)
            label.setScaledContents(True)
            label.setContentsMargins(5, 0, 5, 0)
            label.setAutoFillBackground(True)
            self.participants_layout.addWidget(label)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self, event):
        if event.mimeData().hasText():
            text = event.mimeData().text()
            label = DraggableLabel(text)
            label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
            label.setMargin(2)
            label.setAlignment(Qt.AlignCenter)
            label.setFixedSize(100, 20)
            label.setScaledContents(True)
            label.setContentsMargins(5, 0, 5, 0)
            label.setAutoFillBackground(True)
            self.participants_layout.addWidget(label)
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Group Widget Example")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QGridLayout(central_widget)
        central_widget.setLayout(layout)

        # Create GroupWidgets
        groups_data = [
            ("Group 1", ["Alice", "Bob", "Charlie"]),
            ("Group 2", ["David", "Eve", "Frank"]),
            ("Group 3", ["Grace", "Henry", "Ivy"]),
            ("Group 4", ["Jack", "Kate", "Liam"]),
            ("Group 5", ["Mary", "Nathan", "Olivia"]),
            ("Group 6", ["Peter", "Queen", "Robert"])
        ]
        
        # Populate the grid with GroupWidgets
        row, col = 0, 0
        for title, participants in groups_data:
            group_widget = GroupWidget(title, participants)
            layout.addWidget(group_widget, row, col)
            col += 1
            if col == 3:
                row += 1
                col = 0
        
        # Create DragDropController and connect signals
        self.controller = DragDropController(self, self.findChildren(GroupWidget))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())