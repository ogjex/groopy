import sys
from PyQt6.QtWidgets import QApplication
from ui.workspace_window import WorkspaceWindow

def main():
    app = QApplication(sys.argv)
    
    workspace_window = WorkspaceWindow()

    # Center the window on the screen
    window_width = workspace_window.frameGeometry().width()
    window_height = workspace_window.frameGeometry().height()
    screen = app.primaryScreen()
    screen_width = screen.size().width()
    screen_height = screen.size().height()
    workspace_window.move((screen_width - window_width) // 2, (screen_height - window_height) // 2)
    workspace_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()