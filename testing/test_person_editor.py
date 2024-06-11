import unittest, sys, csv
# setting path
sys.path.append('../groopy')
from person_editor import PersonEditor

class TestPersonEditor(unittest.TestCase):
    def setUp(self):
        self.editor = PersonEditor()

    def test_read_persons_from_csv(self):
        # Assuming the CSV file exists and is correctly formatted
        persons = self.editor.read_persons_from_csv('test_persons.csv')
        self.assertEqual(len(persons), 5)  # Assuming the test file has 5 persons

    def test_shuffle_persons(self):
        persons = self.editor.create_persons_sample()
        shuffled = self.editor.shuffle_persons(persons)
        self.assertNotEqual(persons, shuffled)  # Check if the list order has changed

    def test_get_person_by_id(self):
        persons = self.editor.create_persons_sample()
        person = self.editor.get_person_by_id(1)
        self.assertIsNotNone(person)
        self.assertEqual(person.id, 1)

    def test_get_persons_data_as_dict(self):
        persons = self.editor.create_persons_sample()
        persons_data = self.editor.get_persons_data_as_dict(persons)
        self.assertIsInstance(persons_data, list)
        self.assertIsInstance(persons_data[0], dict)
        self.assertEqual(persons_data[0]['id'], 1)

    def test_save_csv(self):
        persons = self.editor.create_persons_sample()
        self.editor.save_csv(persons, 'test_output.csv')
        # Check if file is created
        with open('test_output.csv', 'r') as file:
            data = file.read()
            self.assertIn('id,name,gender,education,experience,career_preference,desirables,undesirables', data)

if __name__ == '__main__':
    unittest.main()