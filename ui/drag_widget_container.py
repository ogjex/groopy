from PyQt6.QtCore import Qt, QObject, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel
from PyQt6.QtGui import (
    QDragEnterEvent, 
    QDragMoveEvent, 
    QDropEvent, 
    QDragLeaveEvent)
from ui.drag_widget import DragTargetIndicator

class DragWidgetContainer(QWidget, QObject):
    on_order_changed = pyqtSignal(tuple)

    def __init__(self, title: str, id: int, parent=None):
        super().__init__(parent)
        self.title = title
        self.id = id
        self.setAcceptDrops(True)
        self.orientation = Qt.Orientation.Vertical

    def init_ui(self):
        self.layout = QVBoxLayout()
        
        # Create a title label
        self.title_label = QLabel(self.title)
        self.title_label.setMaximumHeight(50)
        self.layout.addWidget(self.title_label)
        
        # Create a frame for participants
        self.dragwidget_frame = QFrame()
        self.dragwidget_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.dragwidget_frame.setFrameShadow(QFrame.Shadow.Sunken)  # Set the shadow of the frame
        self.dragwidget_layout = QVBoxLayout(self.dragwidget_frame)
        self.layout.addWidget(self.dragwidget_frame)

        self.orientation=Qt.Orientation.Vertical
        self._drag_target_indicator = DragTargetIndicator()
        self.dragwidget_layout.addWidget(self._drag_target_indicator)
        self._drag_target_indicator.hide()
        
        self.setLayout(self.layout)
        
        # Show participants initially
        self.dragwidget_frame.show()
        
        # Populate dragwidgets
        self.populate_drag_widgets()
        self.update_height()

    def update_height(self):
        self.setFixedHeight(self.calculate_height())

    def calculate_height():
        ...
    
    def populate_drag_widgets(self):
        ... 
    
    def dragEnterEvent(self, e:QDragEnterEvent):
        e.accept()

    def dragMoveEvent(self, e: QDragMoveEvent):
        # Find the correct location of the drop target, so we can move it there.
        index = self._find_drop_location(e)
        if index is not None:
            # Inserting moves the item if its alreaady in the layout.
            self.dragwidget_layout.insertWidget(index, self._drag_target_indicator)
            # Hide the item being dragged.
            e.source().hide()
            # Show the target.
            self._drag_target_indicator.show()
            self.update_height()
        e.accept()
    
    def dropEvent(self, e: QDropEvent):
        widget = e.source()
        self._drag_target_indicator.hide()
        index = self.dragwidget_layout.indexOf(self._drag_target_indicator)
        if index is not None:
            self.dragwidget_layout.insertWidget(index, widget)
            self.emit_order_changed(widget, self.id)
            widget.show()
            self.dragwidget_layout.activate()
        e.accept()
        self.update_height()

    def emit_order_changed(self, src_widget:QWidget, target_widget_id:int):
        """
        This method emits the on_order_changed signal. It must be overridden by subclasses
        to customize the signal data.
        """
        pass

    def dragLeaveEvent(self, e: QDragLeaveEvent):
        self._drag_target_indicator.hide()
        self.update_height()
        e.accept()

    def _find_drop_location(self, e: QDragMoveEvent):
        pos = e.position()
        spacing = self.dragwidget_layout.spacing() / 2

        for n in range(self.dragwidget_layout.count()):
            # Get the widget at each index in turn.
            w = self.dragwidget_layout.itemAt(n).widget()

            if self.orientation == Qt.Orientation.Vertical:
                # Drag drop vertically.
                drop_here = (
                    pos.y() >= w.y() - spacing
                    and pos.y() <= w.y() + w.size().height() + spacing
                )
            else:
                # Drag drop horizontally.
                drop_here = (
                    pos.x() >= w.x() - spacing
                    and pos.x() <= w.x() + w.size().width() + spacing
                )

            if drop_here:
                # Drop over this target.
                break

        return n