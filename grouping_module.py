import random
from collections import defaultdict
from person import Person
from group import Group

class GroupingModule:
    def __init__(self, people, min_group_size, max_group_size, max_groups_per_person, max_total_groups):
        self.people = people
        self.min_group_size = min_group_size
        self.max_group_size = max_group_size
        self.max_groups_per_person = max_groups_per_person
        self.max_total_groups = max_total_groups
        self.groups = []

    def calculate_optimal_num_groups(self, total_people, min_group_size, max_group_size, max_num_groups) -> int:
        max_possible_num_groups = total_people / min_group_size
        if max_num_groups < max_possible_num_groups:
            max_possible_num_groups = max_num_groups
        min_num_groups_needed = total_people // max_group_size
        return min(min_num_groups_needed, max_possible_num_groups) if total_people % max_group_size == 0 else min(min_num_groups_needed + 1, max_possible_num_groups)

    def count_most_frequent_parameter_value(self, people_list, target_parameter) -> tuple[int, str]:
        parameter_counts = {}
        for person in people_list:
            param_value = getattr(person, target_parameter)  # Get the value of the target parameter for the current person
            if param_value in parameter_counts:
                parameter_counts[param_value] += 1
            else:
                parameter_counts[param_value] = 1
        
        if not parameter_counts:  # If the parameter_counts dictionary is empty
            return 0, None
        
        most_frequent_param_value = max(parameter_counts, key=parameter_counts.get)  # Get the most frequent parameter value
        most_frequent_count = parameter_counts[most_frequent_param_value]  # Get the count of the most frequent parameter value
        return most_frequent_count, most_frequent_param_value
    
    def filter_people_by_parameter(self, people:list[Person], parameter:str, value:str) -> list[Person]:
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
        for person in people:
            # Get the value of the specified parameter for the current person
            person_value = getattr(person, parameter)

            # Check if the person's parameter value matches the desired value
            if person_value == value:
                # If it matches, add the person to the filtered list
                filtered_people.append(person)

        return filtered_people
        
    def group_by_gender(self):
        gender_groups = defaultdict(list)
        for person in self.people:
            gender_groups[person.gender].append(person)
        return gender_groups
    
    def calculate_people_per_group(self, people: list[Person], num_groups: int) -> int:
        num_people_per_group = len(people) // num_groups
        return num_people_per_group

    def group_people_by_education(self, people: list[Person], num_groups: int) -> list[Group]:
        # Create a list of all unique educational backgrounds
        unique_educations = set(person.education for person in people)

        # Calculate the number of people per group
        num_people_per_group = self.calculate_people_per_group(people, num_groups)

        # Shuffle the list of people to introduce randomness
        random.shuffle(people)

        # Initialize the groups list
        groups = [Group() for _ in range(num_groups)]

        # Assign people to groups based on education background
        group_index = 0
        for education in unique_educations:
            # Filter people with the current education background
            people_with_education = [person for person in people if person.education == education]

            # Assign people to groups, ensuring each group receives people with different educational backgrounds
            for person in people_with_education:
                groups[group_index].add_member(person)
                if len(groups[group_index].members) >= num_people_per_group:
                    group_index = (group_index + 1) % num_groups

        return groups