import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QLabel, QFrame, QGridLayout, QMainWindow
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal
from PyQt5.QtGui import QDrag

class DraggableLabel(QLabel):
    dragged = pyqtSignal(str)
    dropped = pyqtSignal()

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
        self.dropped.emit()

class DragDropController:
    def __init__(self, app_window, group_widgets):
        self.app_window = app_window
        self.group_widgets = group_widgets

    def handleDropEvent(self, event):
        print("handledropevent called")
        if self.isInsideApp(event):
            self.handleDropInsideApp(event)
        else:
            self.handleDropOutsideApp(event)

    def isInsideApp(self, event):
        if not event or not self.app_window:            
            return False
        drop_pos = event.pos()
        app_geom = self.app_window.geometry()
        return app_geom.contains(drop_pos)

    def handleDropInsideApp(self, event):
        for group_widget in self.group_widgets:
            if group_widget.geometry().contains(group_widget.mapFromGlobal(event.pos())):
                group_widget.addParticipant(event.mimeData().text())
                event.setDropAction(Qt.MoveAction)
                event.accept()                
                return
        event.ignore()

    def handleDropOutsideApp(self, event):
        event.ignore()

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
        
    def addParticipant(self, participant):
        label = DraggableLabel(participant)
        label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        label.setMargin(2)
        label.setAlignment(Qt.AlignCenter)
        label.setFixedSize(100, 20)
        label.setScaledContents(True)
        label.setContentsMargins(5, 0, 5, 0)
        label.setAutoFillBackground(True)
        self.participants_layout.addWidget(label)
        self.participants.append(participant)

    def removeParticipant(self, participant):
        # Find the label associated with the participant and remove it
        for index in range(self.participants_layout.count()):
            label = self.participants_layout.itemAt(index).widget()
            if label and label.text() == participant:
                label.deleteLater()
                self.participants.remove(participant)
                break  # Break out of the loop once the participant is removed


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Group Widget Example")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QGridLayout()
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
        
        self.group_widgets = []
        for row, (title, participants) in enumerate(groups_data):
            group_widget = GroupWidget(title, participants)
            layout.addWidget(group_widget, row // 3, row % 3)
            self.group_widgets.append(group_widget)
        
        # Create DragDropController and connect dropEvent of the app window
        self.controller = DragDropController(self, self.group_widgets)
        central_widget.dropEvent = self.controller.handleDropEvent
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
