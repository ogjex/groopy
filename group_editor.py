import csv
import json
from typing import List

from group import Group

class GroupEditor:
    def __init__(self):
        self.groups = []
    
    def load_group(group_info):
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

    def read_groups_from_json(filename):
        """
        Read the list of groups from a JSON file.
        
        Args:
        - filename: The filename of the JSON file.
        
        Returns:
        A list of lists where each inner list contains the group name and a list of participants.
        """
        with open(filename, 'r') as json_file:
            data = json.load(json_file)

        groups = [load_group(group_info) for group_info in data["groups"].values()]

        return groups

    def get_group_names(self) -> List[str]:
        """
        Get the list of group names.
        """
        return [group.name for group in self.groups]
    
    def save_groups_to_json(groups, filename):
        """
        Write the list of groups to a JSON file.
        
        Args:
        - groups: A list of tuples where each tuple contains the group name and a list of participants.
        - filename: The filename for the JSON file.
        """
        data = {
            "number_of_groups": len(groups),
            "groups": {}
        }

        for i, (group_name, participants) in enumerate(groups, start=1):
            group_key = f"group{i}"
            data["groups"][group_key] = {
                "name": group_name,
                "participants": participants
            }

        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)

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
