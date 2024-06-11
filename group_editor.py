import json
from typing import List, Tuple, Optional

from person import Person
from person_editor import PersonEditor  
from group import Group
class GroupEditor:
    def __init__(self, person_editor: PersonEditor):
        self.groups = []
        self.person_editor = person_editor
        self.next_id = 1  # Initialize the next_id to 1
    
    def load_group(self, group_info):
        """
        Load a group from JSON data.
        
        Args:
        - group_info: A dictionary containing information about a group.
        
        Returns:
        A list containing the group name and a list of participants.
        """
        group_name = group_info["name"]
        participants = group_info["participants"]
        return [group_name, participants]

    def read_groups_from_json(self, filename):
        """
        Read the list of groups from a JSON file.
        
        Args:
        - filename: The filename of the JSON file.
        
        Returns:
        A list of lists where each inner list contains the group name and a list of participants.
        """
        with open(filename, 'r') as json_file:
            data = json.load(json_file)

        groups = [self.load_group(group_info) for group_info in data["groups"].values()]

        return groups

    def get_group_names(self) -> List[str]:
        """
        Get the list of group names.
        """
        return [group.name for group in self.groups]
    
    def save_groups_to_json(self, filename, persons_csv_path):
        """
        Write the list of groups to a JSON file.

        Args:
        - filename: The filename for the JSON file.
        - persons_csv_path: The path to the persons CSV file.
        """
        # Ensure that the list of groups is created before saving
        if not self.groups:
            raise ValueError("No groups to save.")

        # Create a list of dictionaries containing group id, name, and participants (with IDs only)
        groups_data = [{"id": group.id, "name": group.name, "participants": [person.id for person in group.members]} for group in self.groups]

        # Create a dictionary to store the number of groups, groups' data, and the persons CSV path
        data = {
            "number_of_groups": len(groups_data),
            "groups": {f"group{group['id']}": group for group in groups_data},
            "persons_csv_path": persons_csv_path  # Save path to persons CSV file
        }

        # Save the groups to JSON file
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    
    def create_groups_from_data(self, groups_data: List[Tuple[int, str, List[int]]]):
        """
        Create Group objects from the provided data and add them to the editor.
        
        Args:
        - groups_data: A list of tuples where each tuple contains group data (ID, name, participants).
          The participants are IDs referencing Person objects.
        """
        self.groups.clear()  # Clear existing groups

        # Iterate over the provided group data to create and populate Group objects
        for group_id, group_name, participant_ids in groups_data:
            group = Group(id=group_id, name=group_name)  # Create a new Group object
            for person_id in participant_ids:
                person = self.person_editor.get_person_by_id(person_id)  # Get Person object using PersonEditor
                if person:
                    group.add_member(person)  # Add Person object to the Group
            self.groups.append(group)  # Add the populated Group to the list of groups

            # Ensure next_id is always greater than the highest current ID
            self.next_id = max(self.next_id, group_id + 1)

    def move_person_to_group(self, person_id: int, target_group_id: int) -> bool:
        source_group = self.find_group_of_person(person_id)
        person = self.get_person_by_id(person_id)
        target_group = self.get_group_by_id(target_group_id)

        if source_group and person and target_group:
            source_group.remove_member(person)
            target_group.add_member(person)
            return True
        else:
            return False
        
    def find_group_of_person(self, person_id: int) -> Optional[Group]:
        """
        Find the group that contains the person with the specified ID.

        Args:
            person_id (int): The ID of the person to find.

        Returns:
            Optional[Group]: The group containing the person, or None if not found.
        """
        for group in self.groups:
            for person in group.members:
                if person.id == person_id:
                    return group
        return None
    
    def get_group_by_id(self, group_id: int) -> Optional[Group]:
        """
        Get the group object corresponding to the given ID.

        Args:
            group_id (int): The ID of the group to retrieve.

        Returns:
            Optional[Group]: The group object corresponding to the given ID, or None if not found.
        """
        for group in self.groups:
            if group.id == group_id:
                return group
        return None
    
    def get_person_by_id(self, person_id: int) -> Optional[Person]:
        """
        Get the person object corresponding to the given ID.

        Args:
            person_id (int): The ID of the person to retrieve.

        Returns:
            Optional[Person]: The person object corresponding to the given ID, or None if not found.
        """
        for group in self.groups:
            for person in group.members:
                if person.id == person_id:
                    return person
        return None
    
    def prep_groups_for_view(self) -> List[Tuple[int, str, List[Tuple[int, str]]]]:
        """
        Prepare groups data for the view.

        Returns:
        A list of tuples where each tuple contains group data (ID, name, participants).
        """
        groups_data = []
        for group in self.groups:
            participants = [(person.id, person.name) for person in group.members]
            groups_data.append((group.id, group.name, participants))
        return groups_data

    def create_group_data_sample(self):
        """
        Create sample group data with group IDs and participant IDs using persons from PersonEditor.
        """
        # Ensure PersonEditor has created sample persons
        self.person_editor.create_persons_sample()

        # Create groups using the sample persons created by PersonEditor
        groups_data = [
            ("Group 1", [1, 2, 3]),
            ("Group 2", [4, 5, 6]),
            ("Group 3", [7, 8, 9]),
            ("Group 4", [10, 11, 12]),
            ("Group 5", [13, 14, 15]),
            ("Group 6", [16, 17, 18]),
            ("Group 7", [19, 20, 21]),
            ("Group 8", [22, 23, 24]),
            ("Group 9", [25, 26, 27]),
            ("Group 10", [28, 29, 30])
        ]

        # Add group IDs to each group data tuple
        groups_data_with_ids = [(i + 1, title, participants) for i, (title, participants) in enumerate(groups_data)]
        self.create_groups_from_data(groups_data_with_ids)

    def print_groups(self):
        for g in self.groups:
            print(g)