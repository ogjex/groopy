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
        self.max_total_groups = max_total_groups
        self.groups = []

    def group_by_gender(self):
        gender_groups = defaultdict(list)
        for person in self.people:
            gender_groups[person.gender].append(person)
        return gender_groups
    
    def group_people_by_education(people, num_groups):
        # Create a dictionary to store people based on their university
        university_groups = defaultdict(list)
        for person in people:
            university_groups[person.education].append(person)

        # Calculate the number of people per group
        num_people_per_group = len(people) // num_groups

        # Shuffle the order of people within each university group
        for university, group in university_groups.items():
            random.shuffle(group)

        # Initialize the groups list
        groups = [[] for _ in range(num_groups)]

        # Assign people to groups based on university background
        for university, group in university_groups.items():
            for i, person in enumerate(group):
                groups[i % num_groups].append(person)

        return groups