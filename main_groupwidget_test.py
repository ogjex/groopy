import sys
from PyQt6.QtWidgets import QApplication
from ui.group_window2 import GroupWindow
from group_presenter import GroupPresenter
from group import Group
from person import Person

def main():
    app = QApplication(sys.argv)

    # Create GroupWindow
    group_window = GroupWindow()

    # Create GroupPresenter and link it to GroupWindow
    presenter = GroupPresenter(group_window)

    # Create and add some groups
    group1 = Group("Group 1")
    '''group1.add_member(Person("Alice", "Female", "University A", 3, "Engineering"))
    group1.add_member(Person("Bob", "Male", "University B", 5, "Finance"))
    presenter.add_group(group1)'''
    # Adding a participant to an existing group
    group_name = "Group 1"  # Assuming "Group 1" exists
    participant = Person("Eve", "Female", "University E", 4, "Computer Science")
    presenter.add_participant(group_name, participant)

    group2 = Group("Group 2")
    group2.add_member(Person("Charlie", "Male", "University C", 4, "Marketing"))
    group2.add_member(Person("Diana", "Female", "University D", 6, "HR"))
    presenter.add_group(group2)

    # Show the GroupWindow
    group_window.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()