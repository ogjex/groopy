import random
from collections import defaultdict
from person import Person
from group import Group

class GroupingModule:
    def __init__(self):
        self.groups = []

    def init_group_sort(self, people, min_group_size, max_group_size, max_groups_per_person, max_num_groups):
        self.people = people
        self.min_group_size = min_group_size
        self.max_group_size = max_group_size
        self.max_groups_per_person = max_groups_per_person
        self.max_num_groups = max_num_groups

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
            else:
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

    def create_groups(self, groups_to_create:int) -> list[Group]:
        """
        Creates a list of groups based on the specified input parameter

        Args:
            groups_to_create (int): the amount of groups to create

        Returns:
            list[Group]: the list of groups that people can be added to
        """
        created_groups = []
        for i in range(1, groups_to_create + 1):
            group_name = f"Group {i}"
            created_groups.append(Group(group_name))
        return created_groups
    
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
            
    def find_remainder(self, list1: list[Person], list2: list[Person]) -> list[Person]:
        """
        Find the remainder of Person objects not present in both lists.

        Args:
            list1 (list): The first list of Person objects.
            list2 (list): The second list of Person objects.

        Returns:
            list: A list containing Person objects that are not present in both lists.
        """
        names1 = {person.name for person in list1}
        names2 = {person.name for person in list2}

        unique_names = (names1 ^ names2)

        remainder = []
        for person in list1 + list2:
            if person.name in unique_names:
                remainder.append(person)
        return remainder

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

    def distribute_people_to_groups(self, people_list: list[Person], group_list: list[Group]) -> list[Group]:
        """
        Distribute people to groups iteratively and incrementally.

        This method iterates through the list of people and assigns each person to a group.
        When reaching the end of the group list, it starts over from the beginning.

        Args:
            people_list (list[Person]): List of Person objects.
            group_list (list[Group]): List of Group objects.

        Returns:
            list[Group]: The updated list of groups after distributing people.
        """
        num_people = len(people_list)
        num_groups = len(group_list)

        person_index = 0
        for person in people_list:
            group_index = person_index % num_groups  # Calculate the index of the group for the current person
            current_group = group_list[group_index]  # Get the current group

            # Add the person to the current group
            current_group.add_member(person)

            # Update the group in the list of groups
            group_list[group_index] = current_group

            person_index += 1
            if person_index >= num_people:
                break
        
        return group_list