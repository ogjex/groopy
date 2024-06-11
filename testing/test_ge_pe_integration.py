import unittest
import sys

# setting path
sys.path.append('../groopy')

# setting path
sys.path.append('../groopy')
from group_editor import GroupEditor
from person_editor import PersonEditor

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.person_editor = PersonEditor()
        self.group_editor = GroupEditor(self.person_editor)

    def test_integration(self):
        # Create sample persons and groups
        self.person_editor.create_persons_sample()
        self.group_editor.create_group_data_sample()

        # Check that persons and groups have been created
        self.assertEqual(len(self.person_editor.get_persons()), 20)
        self.assertEqual(len(self.group_editor.groups), 10)

        # Check that groups have members from the persons
        for group in self.group_editor.groups:
            for member in group.members:
                self.assertIsInstance(member, Person)

if __name__ == '__main__':
    unittest.main()