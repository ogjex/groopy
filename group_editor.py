import json
import csv
from typing import List, Tuple

from group import Group
class GroupEditor:
    def __init__(self):
        self.groups = []
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
    
    def save_groups_to_json(self, filename):
        """
        Write the list of groups to a JSON file.
        
        Args:
        - filename: The filename for the JSON file.
        """
        # Ensure that the list of groups is created before saving
        if not self.groups:
            raise ValueError("No groups to save.")

        # Create a list of dictionaries containing group id, name, and participants
        groups_data = [{"id": group.id, "name": group.name, "participants": group.members} for group in self.groups]

        # Create a dictionary to store the number of groups and the groups' data
        data = {
            "number_of_groups": len(groups_data),
            "groups": {f"group{group['id']}": group for group in groups_data}
        }

        # Save the groups to JSON file
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def create_groups_from_data(self, groups_data: List[tuple]) -> List[Group]:
        """
        Create Group objects from the provided data and add them to the editor.
        
        Args:
        - groups_data: A list of tuples where each tuple contains group data (ID, name, participants).
        """
        self.groups.clear()  # Clear existing groups
        for group_id, group_name, participants in groups_data:
            group = Group(id=group_id, name=group_name)
            for participant in participants:
                group.add_member(participant)
            self.groups.append(group)
            # Ensure next_id is always greater than the highest current ID
            self.next_id = max(self.next_id, group_id + 1)

    def find_group(self, group_id: int) -> Group:
        """
        Find a group by ID.
        
        Args:
        - group_id: The ID of the group to find.
        
        Returns:
        The Group object if found, otherwise None.
        """
        for group in self.groups:
            if group.id == group_id:
                return group
        return None

    def create_group_data_sample(self) -> List[Tuple[int, str, List[Tuple[int, str]]]]:
        """
        Create sample group data with group IDs and participant IDs.
        """
        groups_data = [
            ("Group 1", [("Alice", 1), ("Bob", 2), ("Charlie", 3)]),
            ("Group 2", [("David", 4), ("Eve", 5), ("Frank", 6)]),
            ("Group 3", [("Grace", 7), ("Henry", 8), ("Ivy", 9)]),
            ("Group 4", [("Jack", 10), ("Kate", 11), ("Liam", 12)]),
            ("Group 5", [("Mary", 13), ("Nathan", 14), ("Olivia", 15)]),
            ("Group 6", [("Peter", 16), ("Queen", 17), ("Robert", 18)]),
            ("Group 7", [("Henry", 19), ("Norton", 20), ("Moose", 21)]),
            ("Group 8", [("Stan", 22), ("Chao", 23), ("Missy", 24)]),
            ("Group 9", [("Helle", 25), ("Finn", 26), ("Dave", 27)]),
            ("Group 10", [("John", 28), ("Jane", 29), ("Hunny", 30)])
        ]

        # Add group IDs to each group data tuple
        groups_data_with_ids = [(i + 1, title, participants) for i, (title, participants) in enumerate(groups_data)]

        return groups_data_with_ids