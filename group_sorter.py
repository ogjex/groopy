from typing import List, Dict
from person import Person
from group import Group
from collections import defaultdict
import itertools

class GroupSorter:
    def __init__(self, min_group_size=2, max_group_size=5, max_groups_per_person=1, max_num_groups=10):
        self.min_group_size = min_group_size
        self.max_group_size = max_group_size
        self.max_groups_per_person = max_groups_per_person
        self.max_num_groups = max_num_groups
        self.people = []
        self.next_group_id = 1

    def set_min_group_size(self, min_group_size: int):
        self.min_group_size = min_group_size

    def set_max_group_size(self, max_group_size: int):
        self.max_group_size = max_group_size

    def set_max_groups_per_person(self, max_groups_per_person: int):
        self.max_groups_per_person = max_groups_per_person

    def set_max_num_groups(self, max_num_groups: int):
        self.max_num_groups = max_num_groups

    def set_people_to_sort(self, people):
        self.people = people

    def create_groups(self, groups_to_create:int) -> list[Group]:
        """
        Creates a list of groups based on the specified input parameter

        Args:
            groups_to_create (int): the amount of groups to create

        Returns:
            list[Group]: the list of groups that people can be added to
        """
        created_groups = []
        for i in range(groups_to_create):
            group_id = self.next_group_id
            group_name = f"Group {group_id}"
            created_groups.append(Group(id=group_id, name=group_name))
            self.next_group_id += 1  # Increment the next group ID
        return created_groups
    
    def sort_people_by_parameters(self, parameters: List[str]) -> List[Person]:
        """
        Sorts the list of people based on the given parameters.

        Args:
            parameters (List[str]): List of parameters to sort by.

        Returns:
            List[Person]: Sorted list of Person objects.
        """
        sorted_people = self.people[:]
        for param in parameters:
            sorted_people.sort(key=lambda person: getattr(person, param))
        return sorted_people
        
    def distribute_people_to_groups(self, sorted_people: List[Person], strategies: dict[str, str]) -> List[Group]:
        """
        Distributes sorted people into groups based on the given strategies.

        Args:
            sorted_people (List[Person]): List of people sorted by the strategies.
            strategies (dict[str, str]): Dictionary defining the sorting strategy for each parameter.

        Returns:
            List[Group]: List of groups with distributed members.
        """
        # Initialize groups
        self.groups = self.create_groups(self.calculate_optimal_num_groups())
        current_group_index = 0
        
        # Dictionary to store people by parameter value
        parameter_people_dict = {param: {} for param in strategies}
        
        # Populate the dictionaries with people
        for person in sorted_people:
            for param in strategies:
                parameter_value = getattr(person, param)
                if parameter_value not in parameter_people_dict[param]:
                    parameter_people_dict[param][parameter_value] = []
                parameter_people_dict[param][parameter_value].append(person)
        
        # Track which people have already been assigned to a group
        assigned_people = set()
        
        # Distribute people to groups based on strategies
        for param in sorted(strategies.keys()):  # Sort keys to prioritize 'gender' over 'education'
            strategy = strategies[param]
            people_by_value = parameter_people_dict[param]
            
            if strategy == 'focused':
                self.distribute_focused(people_by_value, assigned_people, current_group_index)
            elif strategy == 'spread':
                self.distribute_spread(sorted_people, assigned_people, current_group_index)
        
        # Balance groups to ensure min_group_size
        self.balance_groups()
        
        # Return only non-empty groups
        return [group for group in self.groups if group.members]

    def distribute_focused(self, people_by_value: dict, assigned_people: set, current_group_index: int):
        """
        Distributes people into groups focused (homogeneously) based on the given people_by_value dictionary.

        Args:
            people_by_value (dict): Dictionary containing lists of people grouped by parameter values.
            assigned_people (set): Set of people who have already been assigned to a group.
            current_group_index (int): Current index of the group being processed.
        """
        for value, people_list in people_by_value.items():
            for person in people_list:
                if person not in assigned_people:
                    self.groups[current_group_index].add_member(person)
                    assigned_people.add(person)
                    if len(self.groups[current_group_index].members) >= self.max_group_size:
                        current_group_index += 1
                        if current_group_index >= len(self.groups):
                            current_group_index = 0

    def distribute_spread(self, sorted_people: List[Person], assigned_people: set, current_group_index: int):
        """
        Distributes people into groups spread (heterogeneously) based on the given sorted_people list.

        Args:
            sorted_people (List[Person]): List of people sorted by parameters.
            assigned_people (set): Set of people who have already been assigned to a group.
            current_group_index (int): Current index of the group being processed.
        """
        for person in sorted_people:
            if person not in assigned_people:
                self.groups[current_group_index].add_member(person)
                assigned_people.add(person)
                if len(self.groups[current_group_index].members) >= self.max_group_size:
                    current_group_index += 1
                    if current_group_index >= len(self.groups):
                        current_group_index = 0

    def balance_groups(self):
        """
        Balances the number of members in each group to meet the min_group_size requirement.
        """
        
        for group in self.groups:
            while len(group.members) < self.min_group_size:
                # Find a group with more members than min_group_size
                candidates = [g for g in self.groups if len(g.members) > self.min_group_size]
                if not candidates:
                    break
                candidate = max(candidates, key=lambda g: len(g.members))
                # Move one member from candidate to group
                group.add_member(candidate.members.pop())

    def calculate_optimal_num_groups(self) -> int:
        total_people = len(self.people)
        max_possible_groups = self.calc_max_possible_groups(total_people, self.min_group_size, self.max_num_groups)
        min_num_groups_needed = total_people // self.max_group_size
        return min(min_num_groups_needed, max_possible_groups) if total_people % self.max_group_size == 0 else min(min_num_groups_needed + 1, max_possible_groups)

    def calc_max_possible_groups(self, total_people, min_group_size, max_num_groups):
        max_possible_groups = total_people / min_group_size
        if max_num_groups < max_possible_groups:
            max_possible_groups = max_num_groups
        return max_possible_groups
    
    def count_parameter_occurrences(self, target_parameter:str)->dict:
        """Count the number of paramater and its value occurrences

        Args:
            people_list (Person): takes a list of Person objects
            target_parameter (str): searches for the parameter string

        Returns:
            dict: a dictionary of counts of each parameter
        """
        parameter_counts = {}
        for person in self.people:
            param_value = getattr(person, target_parameter)
            if param_value in parameter_counts:
                parameter_counts[param_value] += 1
                parameter_counts[param_value] = 1
        return parameter_counts
    
    def find_most_frequent_parameter_value(self, parameter_counts:dict)->str:        
        """finds and returns the most frequent value in a dict 

        Args:
            parameter_counts (dict): takes a dictionary as argument

        Returns:
            str: the value of the parameter that occurs the most
        """
        most_frequent_param_value = max(parameter_counts, key=parameter_counts.get)
        return most_frequent_param_value
    
    def filter_people_by_parameter(self, people_list:list[Person], parameter:str, value:str) -> list[Person]:
        """
        Filters a list of Person objects based on the specified parameter and value.

        Args:
            people (list[Person]): List of Person objects.
            parameter (str): The parameter to filter by (e.g., 'education', 'experience', etc.).
            value: The desired value for the specified parameter.

        Returns:
            list[Person]: Filtered list of Person objects.
        """
        filtered_people = []  # Initialize an empty list to store the filtered people

        # Iterate through each person in the input list
        for person in people_list:
            # Get the value of the specified parameter for the current person
            person_value = getattr(person, parameter)

            # Check if the person's parameter value matches the desired value
            if person_value == value:
                # If it matches, add the person to the filtered list
                filtered_people.append(person)

        return filtered_people
            
    def calculate_people_per_group(self, people: list[Person], num_groups: int) -> int:
        """
        Generalised function that calculates people per group and returns the number

        Args:
            people (list[Person]): The list of people to be distributed in groups
            num_groups (int): The number of groups

        Returns:
            int: the number of people to aim for per group
        """
        num_people_per_group = len(people) // num_groups
        return num_people_per_group
    
    def sort_people_by_id(self, people_list: List[Person]) -> List[Person]:
        """
        Sort the list of Person objects based on their IDs.

        Args:
            people_list (List[Person]): The list of Person objects to be sorted.

        Returns:
            List[Person]: The sorted list of Person objects.
        """
        return sorted(people_list, key=lambda person: person.id)