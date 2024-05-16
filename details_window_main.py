import sys
from PyQt6.QtWidgets import QApplication
from person_editor import PersonEditor
from ui.details_window import DetailsWindow

def main():
    # Create PyQt6 application first
    app = QApplication(sys.argv)

    # Instantiate PersonEditor
    person_editor = PersonEditor()

    # Create sample data
    sample_persons = person_editor.create_persons_sample()

    # Prepare sample data as dictionaries
    sample_persons_data = person_editor.get_persons_data_as_dict(sample_persons)

    # Create DetailsWindow instance
    details_window = DetailsWindow()

    # Set sample data in DetailsWindow
    details_window.set_field_values(sample_persons_data)

    # Execute PyQt6 application
    details_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()