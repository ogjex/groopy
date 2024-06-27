import csv, random
from typing import List, Optional
from person import Person

class PersonEditor:
    def __init__(self):
        self.persons = []
        self.reset_id()

    def reset_id(self) -> None:
        """
        Reset the current_id attribute to 1.
        """
        self.current_id = 1

    def next_id(self) -> int:
        next_id = self.current_id
        self.current_id += 1
        return next_id

    def add_person(self, person: Person):
        self.persons.append(person)
    
    def save_csv(self, filename='persons.csv', persons=None):
        if persons is not None:
            self.write_to_csv(persons, filename)
        else:
            self.create_persons_sample()
            self.write_to_csv(filename, self.persons)          

    def write_to_csv(self, filename, person_list):
        fieldnames = ['id', 'name', 'gender', 'education', 'experience', 'career_preference', 'location_preference', 'desirables', 'undesirables']
        with open(filename, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for person in person_list:
                writer.writerow({
                    'id': person.id,
                    'name': person.name,
                    'gender': person.gender,
                    'education': person.education,
                    'experience': person.experience,
                    'career_preference': person.career_preference,
                    'location_preference': person.location_preference,
                    'desirables': ','.join(person.desirables),
                    'undesirables': ','.join(person.undesirables)
                })

    def read_persons_from_csv(self, filename: str) -> List[Person]:
        """
        Read a list of persons from a CSV file.

        Args:
        - filename: The filename of the CSV file.

        Returns:
        A list of Person objects.
        """
        persons = []
        self.reset_id()
        has_id = self.has_id_column(filename)
        with open(filename, 'r', newline='') as csv_file:
            fieldnames = self._get_csv_fieldnames(with_id=has_id)  # Include 'id' if CSV has 'id' column
            csv_reader = csv.DictReader(csv_file, fieldnames=fieldnames)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                person_data = {fieldname: row[fieldname] for fieldname in fieldnames}
                person_data['experience'] = int(person_data['experience'])  # Convert 'experience' to integer
                person_data['desirables'] = person_data['desirables'].split(';') if person_data['desirables'] else []
                person_data['undesirables'] = person_data['undesirables'].split(';') if person_data['undesirables'] else []
                if 'id' in person_data and has_id:
                    person_data['id'] = int(person_data['id'])  # Convert 'id' to integer if present
                else:
                    person_data['id'] = self.next_id()  # Assign the current_id if 'id' is not present
                                
                persons.append(Person(**person_data))  # Pass person_data as kwargs
        self.persons = persons  # Update the persons list in the editor
        return persons

    def has_id_column(self, filename: str, delimiter=',') -> bool:
        """
        Determine if the CSV file has an 'id' column.

        Args:
        - filename: The filename of the CSV file.
        - delimiter: The delimiter used in the CSV file. Default is ','.

        Returns:
        True if the CSV file has an 'id' column, False otherwise.
        """
        with open(filename, 'r', newline='') as csv_file:
            dialect = csv.Sniffer().sniff(csv_file.read(1024), delimiters=delimiter)
            csv_file.seek(0)
            reader = csv.reader(csv_file, dialect)
            headers = next(reader)
            return 'id' in headers

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

    def _get_csv_fieldnames(self, with_id=True) -> List[str]:
        """
        Get the fieldnames structure of the CSV file.

        Args:
        - with_id: Whether to include the 'id' field.

        Returns:
        A list of fieldnames.
        """
        base_fieldnames = ['name', 'gender', 'education', 'experience', 'career_preference', 'location_preference','desirables', 'undesirables']
        if with_id:
            return ['id'] + base_fieldnames
        return base_fieldnames
    
    def get_person_by_id(self, person_id: int) -> Optional[Person]:
        """
        Get the person object corresponding to the given ID.

        Args:
        - person_id: The ID of the person to retrieve.

        Returns:
        The Person object corresponding to the given ID, or None if not found.
        """
        for person in self.persons:
            if person.id == person_id:
                return person
        return None

    def create_persons_sample(self):
        self.persons.clear()
        self.reset_id()
        persons = [
            Person(id=self.next_id(), name="Alice A.", gender="Female", education="Engineering", experience=3, career_preference="Software Development", location_preference="Zealand", desirables=["Bob", "Charlie"]),
            Person(id=self.next_id(), name="Bob", gender="Male", education="Software Engineering", experience=5, career_preference="Software Engineering", location_preference="Zealand", desirables=["Alice"]),
            Person(id=self.next_id(), name="Charlie", gender="Male", education="Mathematics", experience=2, career_preference="Finance", location_preference="Zealand", desirables=["Alice"]),
            Person(id=self.next_id(), name="Eve", gender="Female", education="Engineering", experience=4, career_preference="Software Development", location_preference="Zealand", desirables=["Alice", "Bob"]),
            Person(id=self.next_id(), name="Alice B.", gender="Male", education="Engineering", experience=6, career_preference="Data Science", location_preference="Zealand", desirables=["Alice"]),
            Person(id=self.next_id(), name="Frank", gender="Male", education="Mathematics", experience=1, career_preference="Software Development", location_preference="Jutland"),
            Person(id=self.next_id(), name="Grace", gender="Female", education="Computer Science", experience=4, career_preference="Finance", location_preference="Zealand", desirables=["Bob"]),
            Person(id=self.next_id(), name="Harry", gender="Male", education="Engineering", experience=3, career_preference="Data Science", location_preference="Zealand", desirables=["Alice"]),
            Person(id=self.next_id(), name="Isabel", gender="Female", education="Mathematics", experience=2, career_preference="Software Development", location_preference="Zealand", desirables=["Bob"]),
            Person(id=self.next_id(), name="Jack", gender="Male", education="Engineering", experience=5, career_preference="Finance", location_preference="Zealand", desirables=["Alice"]),
            Person(id=self.next_id(), name="Karen", gender="Female", education="Computer Science", experience=3, career_preference="Data Science", location_preference="Zealand", desirables=["Alice"]),
            Person(id=self.next_id(), name="Liam", gender="Male", education="Engineering", experience=4, career_preference="Software Development", location_preference="Jutland"),
            Person(id=self.next_id(), name="Mia", gender="Female", education="Mathematics", experience=5, career_preference="Data Science", location_preference="Zealand", desirables=["Charlie"]),
            Person(id=self.next_id(), name="Nathan", gender="Male", education="Engineering", experience=3, career_preference="Finance", location_preference="Zealand", desirables=["Alice"]),
            Person(id=self.next_id(), name="Olivia", gender="Female", education="Computer Science", experience=2, career_preference="Software Development", location_preference="Zealand", desirables=["Bob"]),
            Person(id=self.next_id(), name="Peter", gender="Male", education="Mathematics", experience=4, career_preference="Data Science", location_preference="Zealand", desirables=["Alice"]),
            Person(id=self.next_id(), name="Quinn", gender="Female", education="Engineering", experience=3, career_preference="Finance", location_preference="Zealand", desirables=["Alice"]),
            Person(id=self.next_id(), name="Robert", gender="Male", education="Computer Science", experience=2, career_preference="Software Development", location_preference="Zealand", desirables=["Alice"]),
            Person(id=self.next_id(), name="Sophia", gender="Female", education="Mathematics", experience=4, career_preference="Data Science", location_preference="Zealand", desirables=["Charlie"]),
            Person(id=self.next_id(), name="Thomas", gender="Male", education="Engineering", experience=5, career_preference="Finance", location_preference="Virtual"),
            Person(id=self.next_id(), name="Hortensia", gender="Female", education="Economics", experience=5, career_preference="Finance", location_preference="Virtual")
        ]
        for person in persons: 
                self.add_person(person)
    
    # Example usage
if __name__ == "__main__":
    editor = PersonEditor()
    editor.save_csv("persons.csv")
    