import csv
import json
from typing import List

from person import Person
from group import Group

class GroupEditor:
    def __init__(self):
        self.groups = []
    
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

    def read_group_from_csv(self, filename: str, group_name: str):
        """
        Read data (persons) from a CSV file and load them into a group.
        """
        group = self.find_group(group_name)
        if not group:
            group = Group(group_name)
            self.groups.append(group)
        group.read_from_csv(filename)

    def save_group_to_csv(self, filename: str, group_name: str):
        """
        Save data (persons) from a group to a CSV file.
        """
        group = self.find_group(group_name)
        if group:
            group.save_to_csv(filename)

    def create_group_names_json(self, filename: str):
        """
        Create a JSON file with the list of group names.
        """
        group_names = [group.name for group in self.groups]
        with open(filename, 'w') as json_file:
            json.dump(group_names, json_file)

    def get_group_names(self) -> List[str]:
        """
        Get the list of group names.
        """
        return [group.name for group in self.groups]