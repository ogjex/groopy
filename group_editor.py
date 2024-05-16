import json
import csv
from typing import List

from group import Group
class GroupEditor:
    def __init__(self):
        self.groups = []
    
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

        # Create a list of lists containing group name and participants
        groups_data = [[group.name, group.members] for group in self.groups]

        # Create a dictionary to store the number of groups and the groups' data
        data = {
            "number_of_groups": len(groups_data),
            "groups": {}
        }

        # Populate the dictionary with group data
        for i, (group_name, participants) in enumerate(groups_data, start=1):
            group_key = f"group{i}"
            data["groups"][group_key] = {
                "name": group_name,
                "participants": participants
            }

        # Save the groups to JSON file
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def create_groups_from_data(self, groups_data: List[list]) -> List[Group]:
        """
        Create Group objects from the provided data and add them to the editor.
        
        Args:
        - groups_data: A list of lists where each inner list contains group data.
        """
        self.groups.clear()  # Clear existing groups
        for group_info in groups_data:
            group_name, participants = group_info
            group = Group(group_name)
            for participant in participants:
                group.add_member(participant)
            self.groups.append(group)

    def find_group(self, group_name: str) -> Group:
        """_summary_

        Args:
            group_name (str): _description_

        Returns:
            Group: _description_
        """
        for group in self.groups:
            if group.name == group_name:
                return group
        return None
