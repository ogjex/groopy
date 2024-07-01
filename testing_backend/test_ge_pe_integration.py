import csv
import unittest
import sys
from typing import List

# setting path
sys.path.append('../groopy')
from group_editor import GroupEditor
from person_editor import PersonEditor
from person import Person

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.person_editor = PersonEditor()
        self.group_editor = GroupEditor(self.person_editor)

    def test_integration(self):
        # Create sample persons and groups
        self.person_editor.create_persons_sample()
        self.group_editor.create_group_data_sample()
    def save_csv(self, persons=None, filename='persons.csv'):
        if persons is not None:
            self._save_persons_to_csv(persons, filename)
        else:
            persons_sample = self.create_persons_sample()
            self._save_persons_to_csv(persons_sample, filename)

    def _save_persons_to_csv(self, persons: List[Person], filename: str):
        """
        Save the list of persons to a CSV file.

        Args:
        - persons: A list of Person objects.
        - filename: The filename of the CSV file.
        """
        with open(filename, 'w', newline='') as csv_file:
            fieldnames = self._get_csv_fieldnames()
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()
            for person in persons:
                row_data = {fieldname: getattr(person, fieldname.lower()) for fieldname in fieldnames}
                csv_writer.writerow(row_data)

        # Check that persons and groups have been created
        self.assertEqual(len(self.person_editor.get_persons()), 20)
        self.assertEqual(len(self.group_editor.groups), 10)

        # Check that groups have members from the persons
        for group in self.group_editor.groups:
            for member in group.members:
                self.assertIsInstance(member, Person)

if __name__ == '__main__':
    unittest.main()