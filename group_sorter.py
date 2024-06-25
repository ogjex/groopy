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
        Sort people based on multiple parameters.

        Args:
            parameters (List[str]): List of parameter names to sort by in priority order.

        Returns:
            List[Person]: Sorted list of people.
        """
        return sorted(self.people, key=lambda person: tuple(getattr(person, param) for param in parameters))

    def distribute_people_to_groups(self, sorted_people, strategies):
        # Calculate the optimal number of groups
        optimal_num_groups = self.calculate_optimal_num_groups()
        print(f"{optimal_num_groups}")
        # Initialize groups
        self.groups = [Group(id=i+1, name=f'Group {i+1}') for i in range(optimal_num_groups)]
        
        current_group_index = 0
        
        # Create dictionaries to store people based on the strategy
        parameter_people_dict = {param: {} for param in strategies}
        
        # Populate the dictionaries with people
        for person in sorted_people:
            for param in strategies:
                parameter_value = getattr(person, param)
                if parameter_value not in parameter_people_dict[param]:
                    parameter_people_dict[param][parameter_value] = []
                parameter_people_dict[param][parameter_value].append(person)
        
        for param, strategy in strategies.items():
            people_by_value = parameter_people_dict[param]
            
            if strategy == 'homogeneous':
                for value, people_list in people_by_value.items():
                    for person in people_list:
                        self.groups[current_group_index].add_member(person)
                        if len(self.groups[current_group_index].members) >= self.max_group_size:
                            current_group_index += 1
                            if current_group_index >= len(self.groups):
                                current_group_index = 0  # Start reusing groups if we exceed the max number of groups
            elif strategy == 'heterogeneous':
                while any(people_by_value.values()):
                    for value, people_list in people_by_value.items():
                        if people_list:
                            self.groups[current_group_index].add_member(people_list.pop(0))
                            if len(self.groups[current_group_index].members) >= self.max_group_size:
                                current_group_index += 1
                                if current_group_index >= len(self.groups):
                                    current_group_index = 0
        
        self.balance_groups()
        
        # Return only non-empty groups
        return [group for group in self.groups if group.members]

    def balance_groups(self):
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