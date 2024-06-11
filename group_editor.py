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
    
    def create_groups_from_data(self, groups_data: List[Tuple[int, str, List[Tuple[int, str]]]]):
        """
        Create Group objects from the provided data and add them to the editor.
        
        Args:
        - groups_data: A list of tuples where each tuple contains group data (ID, name, participants).
          The participants are tuples containing (participant_id, participant_name).
        """
        self.groups.clear()  # Clear existing groups
        for group_id, group_name, participant_ids in groups_data:
            group = Group(id=group_id, name=group_name)
            for person_id in participant_ids:
                person = self.person_editor.get_person_by_id(person_id)  # Get Person object using PersonEditor
                if person:
                    group.add_member(person)
            self.groups.append(group)
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

    def create_group_data_sample(self):# -> List[Tuple[int, str, List[Tuple[int, str]]]]:
        """
        Create sample group data with group IDs and participant IDs.
        """
        groups_data = [
            ("Group 1", [(1, "Alice"), (2, "Bob"), (3, "Charlie")]),
            ("Group 2", [(4, "David"), (5, "Eve"), (6, "Frank")]),
            ("Group 3", [(7, "Grace"), (8, "Henry"), (9, "Ivy")]),
            ("Group 4", [(10, "Jack"), (11, "Kate"), (12, "Liam")]),
            ("Group 5", [(13, "Mary"), (14, "Nathan"), (15, "Olivia")]),
            ("Group 6", [(16, "Peter"), (17, "Queen"), (18, "Robert")]),
            ("Group 7", [(19, "Henry"), (20, "Norton"), (21, "Moose")]),
            ("Group 8", [(22, "Stan"), (23, "Chao"), (24, "Missy")]),
            ("Group 9", [(25, "Helle"), (26, "Finn"), (27, "Dave")]),
            ("Group 10", [(28, "John"), (29, "Jane"), (30, "Hunny")])
        ]

        # Add group IDs to each group data tuple
        groups_data_with_ids = [(i + 1, title, participants) for i, (title, participants) in enumerate(groups_data)]
        self.create_groups_from_data(groups_data_with_ids)
        #return groups_data_with_ids

    def print_groups(self):
        for g in self.groups:
            print(g)