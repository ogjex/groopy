from typing import List
from person import Person
from group import Group

class GroupSorter:
    def __init__(self, min_group_size=2, max_group_size=5, max_groups_per_person=1, max_num_groups=10):
        # Initialize default values
        self.min_group_size = min_group_size
        self.max_group_size = max_group_size
        self.max_groups_per_person = max_groups_per_person
        self.max_num_groups = max_num_groups
        self.people = []
        self.next_group_id = 1
        self.current_group_index = 0
        self.assigned_people = set()

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
        for i in range(groups_to_create):
            group_id = self.next_group_id
            group_name = f"Group {group_id}"
            created_groups.append(Group(id=group_id, name=group_name))
            self.next_group_id += 1  # Increment the next group ID
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
            
    def find_remainder(self, list1: List[Person], list2: List[Person]) -> List[Person]:
        """
        Find the remainder of Person objects not present in both lists.

        Args:
            list1 (List[Person]): The first list of Person objects.
            list2 (List[Person]): The second list of Person objects.

        Returns:
            List[Person]: A list containing Person objects that are not present in both lists.
        """
        # Create a set of IDs for the second list
        ids2 = {person.id for person in list2}
        
        # Filter out the persons in list1 that are not in list2
        remainder = [person for person in list1 if person.id not in ids2]
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
            group_index = self.current_group_index % num_groups  # Calculate the index of the group for the current person
            current_group = group_list[group_index]  # Get the current group

            # Add the person to the current group
            current_group.add_member(person)

            # Update the group in the list of groups
            group_list[group_index] = current_group

            self.current_group_index += 1  # Update the current group index

            person_index += 1
            if person_index >= num_people:
                break
        
        return group_list
    
    def focus_people_on_parameter(self, parameter: str) -> list[Group]:
        """
        Groups people based on a single parameter to create homogeneous groups.

        This method sorts people based on the specified parameter and distributes them into groups
        by filling up one group at a time until the maximum group size is reached, then moves to the next group.

        Args:
            parameter (str): The parameter to focus on (e.g., 'education', 'experience', etc.).

        Returns:
            list[Group]: The list of groups after distributing people based on the specified parameter.
        """
        # Count the occurrences of each value for the specified parameter
        param_counts = self.count_parameter_occurrences(parameter)
        
        # Sort parameter values by their frequency in descending order
        sorted_param_values = sorted(param_counts, key=param_counts.get, reverse=True)
        
        # Create the optimal number of groups
        optimal_num_groups = self.calculate_optimal_num_groups()
        group_list = self.create_groups(optimal_num_groups)
        
        # Clear the assigned_people set
        self.assigned_people.clear()

        # Iterate over sorted parameter values and distribute people into groups
        for value in sorted_param_values:
            filtered_people = self.filter_people_by_parameter(self.people, parameter, value)
            
            # Distribute people into groups by filling one group at a time
            for person in filtered_people:
                for group in group_list:
                    if len(group.members) < self.max_group_size:
                        group.add_member(person)
                        self.assigned_people.add(person)
                        break
        
        # Find the remainder of the people who were not assigned to any group
        remainder_people = self.find_remainder(self.people, self.assigned_people)
        
        # Distribute the remainder of the people into groups
        for person in remainder_people:
            for group in group_list:
                if len(group.members) < self.max_group_size:
                    group.add_member(person)
                    break
        
        return group_list
    
    def dynamic_sort_and_group(self, parameters: list[str]):
        optimal_num_groups = self.calculate_optimal_num_groups()
        group_list = self.create_groups(optimal_num_groups)

        sorted_people = self.sort_people_by_id(self.people)
        for param in parameters:
            param_counts = self.count_parameter_occurrences(param)
            most_frequent_value = self.find_most_frequent_parameter_value(param_counts)
            filtered_people = self.filter_people_by_parameter(sorted_people, param, most_frequent_value)
            remainder_people = self.find_remainder(sorted_people, filtered_people)
            group_list = self.distribute_people_to_groups(filtered_people, group_list)
            sorted_people = remainder_people

        group_list = self.distribute_people_to_groups(sorted_people, group_list)
        return group_list
    
    def sort_people_by_id(self, people_list: List[Person]) -> List[Person]:
        """
        Sort the list of Person objects based on their IDs.

        Args:
            people_list (List[Person]): The list of Person objects to be sorted.

        Returns:
            List[Person]: The sorted list of Person objects.
        """
        return sorted(people_list, key=lambda person: person.id)