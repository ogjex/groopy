import csv, random
from typing import List
from person import Person

class PersonEditor:
    def __init__(self):
        self.persons = []
        self.next_id = 1  # Initialize the next_id to 1

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
            fieldnames = self._get_csv_fieldnames(with_id=False)  # Exclude 'id' from fieldnames for reading
            csv_reader = csv.DictReader(csv_file, fieldnames=fieldnames)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                person_data = {fieldname: row[fieldname] for fieldname in fieldnames}
                person_data['experience'] = int(person_data['experience'])  # Convert 'experience' to integer
                person_data['desirables'] = person_data['desirables'].split(';') if person_data['desirables'] else []
                person_data['undesirables'] = person_data['undesirables'].split(';') if person_data['undesirables'] else []
                person_data['id'] = self.next_id  # Assign the next_id
                persons.append(Person(**person_data))
                self.next_id += 1  # Increment next_id for the next person
        self.persons = persons  # Update the persons list in the editor
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
    
    def _get_csv_fieldnames(self, with_id=True) -> List[str]:
        """
        Get the fieldnames structure of the CSV file.

        Args:
        - with_id: Whether to include the 'id' field.

        Returns:
        A list of fieldnames.
        """
        base_fieldnames = ['name', 'gender', 'education', 'experience', 'career_preference', 'desirables', 'undesirables']
        if with_id:
            return ['id'] + base_fieldnames
        return base_fieldnames
    
    def create_persons_sample(self) -> List[Person]:
        persons = [
            Person(id=self.next_id, name="Alice A.", gender="Female", education="Engineering", experience=3, career_preference="Software Development", desirables=["Bob", "Charlie"]),
            Person(id=self.next_id + 1, name="Bob", gender="Male", education="Software Engineering", experience=5, career_preference="Software Engineering", desirables=["Alice"]),
            Person(id=self.next_id + 2, name="Charlie", gender="Male", education="Mathematics", experience=2, career_preference="Finance", desirables=["Alice"]),
            Person(id=self.next_id + 3, name="Eve", gender="Female", education="Engineering", experience=4, career_preference="Software Development", desirables=["Alice", "Bob"]),
            Person(id=self.next_id + 4, name="Alice B.", gender="Male", education="Engineering", experience=6, career_preference="Data Science", desirables=["Alice"]),
            Person(id=self.next_id + 5, name="Frank", gender="Male", education="Mathematics", experience=1, career_preference="Software Development"),
            Person(id=self.next_id + 6, name="Grace", gender="Female", education="Computer Science", experience=4, career_preference="Finance", desirables=["Bob"]),
            Person(id=self.next_id + 7, name="Harry", gender="Male", education="Engineering", experience=3, career_preference="Data Science", desirables=["Alice"]),
            Person(id=self.next_id + 8, name="Isabel", gender="Female", education="Mathematics", experience=2, career_preference="Software Development", desirables=["Bob"]),
            Person(id=self.next_id + 9, name="Jack", gender="Male", education="Engineering", experience=5, career_preference="Finance", desirables=["Alice"]),
            Person(id=self.next_id + 10, name="Karen", gender="Female", education="Computer Science", experience=3, career_preference="Data Science", desirables=["Alice"]),
            Person(id=self.next_id + 11, name="Liam", gender="Male", education="Engineering", experience=4, career_preference="Software Development"),
            Person(id=self.next_id + 12, name="Mia", gender="Female", education="Mathematics", experience=5, career_preference="Data Science", desirables=["Charlie"]),
            Person(id=self.next_id + 13, name="Nathan", gender="Male", education="Engineering", experience=3, career_preference="Finance", desirables=["Alice"]),
            Person(id=self.next_id + 14, name="Olivia", gender="Female", education="Computer Science", experience=2, career_preference="Software Development", desirables=["Bob"]),
            Person(id=self.next_id + 15, name="Peter", gender="Male", education="Mathematics", experience=4, career_preference="Data Science", desirables=["Alice"]),
            Person(id=self.next_id + 16, name="Quinn", gender="Female", education="Engineering", experience=3, career_preference="Finance", desirables=["Alice"]),
            Person(id=self.next_id + 17, name="Robert", gender="Male", education="Computer Science", experience=2, career_preference="Software Development", desirables=["Alice"]),
            Person(id=self.next_id + 18, name="Sophia", gender="Female", education="Mathematics", experience=4, career_preference="Data Science", desirables=["Charlie"]),
            Person(id=self.next_id + 19, name="Thomas", gender="Male", education="Engineering", experience=5, career_preference="Finance"),
            Person(id=self.next_id + 20, name="Hortensia", gender="Female", education="Economics", experience=5, career_preference="Finance")                
            ]
        self.next_id += len(persons)  # Increment next_id by the number of persons added
        self.persons = persons
        return persons