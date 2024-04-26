import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QLabel, QFrame, QGridLayout, QMainWindow
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal
from PyQt5.QtGui import QDrag

class DraggableLabel(QLabel):
    dragged = pyqtSignal(str)

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
            label.dragged.connect(self.removeParticipant)  # Connect signal to removeParticipant slot
            self.participants_layout.addWidget(label)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self, event):
        if event.mimeData().hasText():
            text = event.mimeData().text()
            sender = self.sender()

            # Check if the drop event occurred within any group widget
            group_widgets = self.window().findChildren(GroupWidget)
            for group_widget in group_widgets:
                if group_widget.geometry().contains(event.pos()):
                    # If the sender is not a GroupWidget or it's not the parent of the event source,
                    # then the participant is being dragged from outside this group widget
                    if not isinstance(sender, GroupWidget) or sender.parent() != group_widget:
                        # Add the participant only if it's not already in this group
                        if text not in group_widget.participants:
                            label = DraggableLabel(text)
                            label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
                            label.setMargin(2)
                            label.setAlignment(Qt.AlignCenter)
                            label.setFixedSize(100, 20)
                            label.setScaledContents(True)
                            label.setContentsMargins(5, 0, 5, 0)
                            label.setAutoFillBackground(True)
                            label.dragged.connect(group_widget.removeParticipant)  # Connect signal to removeParticipant slot
                            group_widget.participants_layout.addWidget(label)
                            group_widget.participants.append(text)
                        event.setDropAction(Qt.MoveAction)
                        event.accept()
                    return  # Exit the loop if a group widget contains the drop event

            # If the drop event didn't occur within any group widget, ignore it
            event.ignore()
        else:
            event.ignore()



    def removeParticipant(self, participant):
        sender = self.sender()
        if sender and isinstance(sender, DraggableLabel):
            # Remove the dragged label from the layout
            sender.deleteLater()

            # Remove the participant from the list only if it exists in the list
            if participant in self.participants:
                self.participants.remove(participant)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Group Widget Example")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        '''layout = QVBoxLayout(central_widget)
        
        # Create a button to toggle visibility of all participants
        self.toggle_button = QPushButton("Hide Participants")
        self.toggle_button.clicked.connect(self.toggleParticipants)
        layout.addWidget(self.toggle_button)'''

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
        
        # Populate the grid with GroupWidgets
        row, col = 0, 0
        for title, participants in groups_data:
            group_widget = GroupWidget(title, participants)
            layout.addWidget(group_widget, row, col)
            col += 1
            if col == 3:
                row += 1
                col = 0
    
    def toggleParticipants(self):
        # Toggle visibility of all participants in all groups
        if self.toggle_button.text() == "Hide Participants":
            self.toggle_button.setText("Show Participants")
            for widget in self.findChildren(GroupWidget):
                widget.participants_frame.hide()
        else:
            self.toggle_button.setText("Hide Participants")
            for widget in self.findChildren(GroupWidget):
                widget.participants_frame.show()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
