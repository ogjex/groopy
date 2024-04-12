import random
from collections import defaultdict
from itertools import combinations
from person import Person
from group import Group

class GroupingModule:
    def __init__(self, people, min_group_size, max_group_size, max_groups_per_person, max_total_groups):
        self.people = people
        self.min_group_size = min_group_size
        self.max_group_size = max_group_size
        self.max_groups_per_person = max_groups_per_person
        self.groups = []

    def calculate_optimal_num_groups(self, total_people, max_group_size, max_num_groups) -> int:
        max_possible_num_groups = total_people / self.min_group_size
        if max_num_groups < max_possible_num_groups:
            max_possible_num_groups = max_num_groups
        max_people_allowed = max_group_size * max_num_groups
        min_num_groups_needed = total_people // max_group_size
        return min(min_num_groups_needed, max_possible_num_groups) if total_people % max_group_size == 0 else min(min_num_groups_needed + 1, max_possible_num_groups)

    def group_by_gender(self):
        gender_groups = defaultdict(list)
        for person in self.people:
            gender_groups[person.gender].append(person)
        return gender_groups
    
    def group_people_by_education(self, people, num_groups):
        # Create a dictionary to store people based on their education
        education_groups = defaultdict(list)
        for person in people:
            education_groups[person.education].append(person)

        # Calculate the number of people per group
        num_people_per_group = len(people) // num_groups

        # Shuffle the order of people within each education group
        for education, group in education_groups.items():
            random.shuffle(group)

        # Initialize the groups listS
        groups = [[] for _ in range(num_groups)]

        # Assign people to groups based on university background
        for education, group in education_groups.items():
            for i, person in enumerate(group):
                groups[i % num_groups].append(person)

        return groups