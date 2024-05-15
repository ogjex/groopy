import csv
from typing import List
from person import Person

class PersonEditor:
    def __init__(self):
        pass

    def read_persons_from_csv(self, filename: str) -> List[Person]:
        """
        Read a list of persons from a CSV file.

        Args:
        - filename: The filename of the CSV file.

        Returns:
        A list of Person objects.
        """
        persons = []
        with open(filename, 'r', newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                # Create a Person object from CSV row data
                person = Person(
                    name=row['Name'],
                    gender=row['Gender'],
                    education=row['Education'],
                    experience=row['Experience'],
                    career_preference=row['Career Preference'],
                    desirables=row.get('Desirables', '').split(';') if 'Desirables' in row else None,
                    undesirables=row.get('Undesirables', '').split(';') if 'Undesirables' in row else None
                )
                persons.append(person)
        return persons
