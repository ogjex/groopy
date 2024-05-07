import sys
from PyQt6.QtWidgets import QApplication
from buttonEditor import ButtonEditor
from ButtonPresenter import Presenter
from buttonWidget import ColorButtonWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ColorButtonWidget()
    buttonEditor = ButtonEditor()
    presenter = Presenter(buttonEditor, window)
    presenter.run()
    sys.exit(app.exec())
