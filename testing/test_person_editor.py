import unittest, sys, csv
# setting path
sys.path.append('../groopy')
from person_editor import PersonEditor
from person import Person
import os

class TestPersonEditor(unittest.TestCase):
    def setUp(self):
        # Create a sample CSV file for testing
        with open('test_persons.csv', 'w', newline='') as csvfile:
            fieldnames = ['Name', 'Gender', 'Education', 'Experience', 'Career Preference', 'Desirables', 'Undesirables']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'Name': 'Alice', 'Gender': 'Female', 'Education': 'Engineering', 'Experience': '3', 'Career Preference': 'Software Development', 'Desirables': 'Bob;Charlie', 'Undesirables': ''})
            writer.writerow({'Name': 'Bob', 'Gender': 'Male', 'Education': 'Software Engineering', 'Experience': '5', 'Career Preference': 'Software Engineering', 'Desirables': 'Alice', 'Undesirables': ''})
            # Add more sample rows if needed

    def test_read_persons_from_csv(self):
        editor = PersonEditor()
        persons = editor.read_persons_from_csv('test_persons.csv')
        
        # Check if the correct number of Person objects are read
        self.assertEqual(len(persons), 2)

        # Check if the first Person object is read correctly
        self.assertEqual(persons[0].name, 'Alice')
        self.assertEqual(persons[0].gender, 'Female')
        self.assertEqual(persons[0].education, 'Engineering')
        self.assertEqual(persons[0].experience, 3)
        self.assertEqual(persons[0].career_preference, 'Software Development')
        self.assertEqual(persons[0].desirables, ['Bob', 'Charlie'])
        self.assertEqual(persons[0].undesirables, [])

        # Check if the second Person object is read correctly
        self.assertEqual(persons[1].name, 'Bob')
        self.assertEqual(persons[1].gender, 'Male')
        self.assertEqual(persons[1].education, 'Software Engineering')
        self.assertEqual(persons[1].experience, 5)
        self.assertEqual(persons[1].career_preference, 'Software Engineering')
        self.assertEqual(persons[1].desirables, ['Alice'])
        self.assertEqual(persons[1].undesirables, [])

    def tearDown(self):
        # Clean up the sample CSV file after the test
        os.remove('test_persons.csv')

if __name__ == '__main__':
    unittest.main()
