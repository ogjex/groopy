import csv, random
from typing import List
from person import Person

class PersonEditor:
    def __init__(self):
        self.persons = []

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
            fieldnames = self._get_csv_fieldnames()
            csv_reader = csv.DictReader(csv_file, fieldnames=fieldnames)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                person_data = {fieldname: row[fieldname] for fieldname in fieldnames}
                # Convert 'experience' to integer
                person_data['experience'] = int(person_data['experience'])
                # Split 'desirables' into a list
                person_data['desirables'] = person_data['desirables'].split(';') if person_data['desirables'] else []
                # Handle empty 'undesirables'
                person_data['undesirables'] = person_data['undesirables'].split(';') if person_data['undesirables'] else []
                persons.append(Person(**person_data))
        return persons

    def shuffle_persons(self, persons: List[Person]) -> List[Person]:
        """
        Shuffle the list of persons randomly.

        Args:
        - persons: A list of Person objects.

        Returns:
        A shuffled list of Person objects.
        """
        shuffled_persons = persons[:]
        random.shuffle(shuffled_persons)
        return shuffled_persons
    
    def get_persons(self) -> List[Person]:
        return self.persons
    
    def get_persons_data_as_dict(self, persons: List[Person]) -> List[dict]:
        """
        Convert a list of Person objects into a list of dictionaries.

        Args:
        - persons: A list of Person objects.

        Returns:
        A list of dictionaries containing person data.
        """
        fieldnames = self._get_csv_fieldnames()
        persons_data = []
        for person in persons:
            person_data = {fieldname: getattr(person, fieldname.lower(), "") for fieldname in fieldnames}
            persons_data.append(person_data)
        return persons_data

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
    
    def _get_csv_fieldnames(self) -> List[str]:
        """
        Get the fieldnames structure of the CSV file.

        Returns:
        A list of fieldnames.
        """
        return ['name', 'gender', 'education', 'experience', 'career_preference', 'desirables', 'undesirables']

    def create_persons_sample(self) -> List[Person]:
        persons = [
            Person(name="Alice A.", gender="Female", education="Engineering", experience=3, career_preference="Software Development", desirables=["Bob", "Charlie"]),
            Person(name="Bob", gender="Male", education="Software Engineering", experience=5, career_preference="Software Engineering", desirables=["Alice"]),
            Person(name="Charlie", gender="Male", education="Mathematics", experience=2, career_preference="Finance", desirables=["Alice"]),
            Person(name="Eve", gender="Female", education="Engineering", experience=4, career_preference="Software Development", desirables=["Alice", "Bob"]),
            Person(name="Alice B.", gender="Male", education="Engineering", experience=6, career_preference="Data Science", desirables=["Alice"]),
            Person(name="Frank", gender="Male", education="Mathematics", experience=1, career_preference="Software Development"),
            Person(name="Grace", gender="Female", education="Computer Science", experience=4, career_preference="Finance", desirables=["Bob"]),
            Person(name="Harry", gender="Male", education="Engineering", experience=3, career_preference="Data Science", desirables=["Alice"]),
            Person(name="Isabel", gender="Female", education="Mathematics", experience=2, career_preference="Software Development", desirables=["Bob"]),
            Person(name="Jack", gender="Male", education="Engineering", experience=5, career_preference="Finance", desirables=["Alice"]),
            Person(name="Karen", gender="Female", education="Computer Science", experience=3, career_preference="Data Science", desirables=["Alice"]),
            Person(name="Liam", gender="Male", education="Engineering", experience=4, career_preference="Software Development"),
            Person(name="Mia", gender="Female", education="Mathematics", experience=5, career_preference="Data Science", desirables=["Charlie"]),
            Person(name="Nathan", gender="Male", education="Engineering", experience=3, career_preference="Finance", desirables=["Alice"]),
            Person(name="Olivia", gender="Female", education="Computer Science", experience=2, career_preference="Software Development", desirables=["Bob"]),
            Person(name="Peter", gender="Male", education="Mathematics", experience=4, career_preference="Data Science", desirables=["Alice"]),
            Person(name="Quinn", gender="Female", education="Engineering", experience=3, career_preference="Finance", desirables=["Alice"]),
            Person(name="Robert", gender="Male", education="Computer Science", experience=2, career_preference="Software Development", desirables=["Alice"]),
            Person(name="Sophia", gender="Female", education="Mathematics", experience=4, career_preference="Data Science", desirables=["Charlie"]),
            Person(name="Thomas", gender="Male", education="Engineering", experience=5, career_preference="Finance"),
            Person(name="Hortensia", gender="Female", education="Economics", experience=5, career_preference="Finance")                
            ]
        self.persons = persons
        return persons