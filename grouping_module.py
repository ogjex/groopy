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
    
    def group_people_by_university(people, num_groups):
        # Create a dictionary to store people based on their university
        university_groups = defaultdict(list)
        for person in people:
            university_groups[person.university].append(person)

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

    def sort_people_by_undesirables(self, people):
        # Sort people based on the number of undesirables
        sorted_people = sorted(people, key=lambda x: len(x.undesirables), reverse=True)

        # Ensure that sorting does not exceed the maximum number of groups
        max_groups_needed = max(len(people) // len(set(len(person.undesirables) for person in people)), 1)
        sorted_people = sorted_people[:max_groups_needed * self.max_total_groups]

        return sorted_people

    def sort_people(self, people, gender, university):
        # Sort people based on undesirables first
        sorted_people = sorted(people, key=lambda x: len(x.undesirables), reverse=True)
        
        # Sort by mutual desirables
        sorted_people = sorted(sorted_people, key=lambda x: (len(set(x.desirables) & set([p.name for p in people]))), reverse=True)
        
        # Sort by different universities
        sorted_people = sorted(sorted_people, key=lambda x: x.university)
        
        # Sort by gender
        sorted_people = sorted(sorted_people, key=lambda x: x.gender)
        
        return sorted_people

    def group_by_university(self, people):
        university_groups = defaultdict(list)
        for person in people:
            university_groups[person.university].append(person)
        return university_groups

    def assign_groups(self):
        gender_groups = self.group_by_gender()
        for gender, people_group in gender_groups.items():
            people_group = self.sort_people(people_group, gender, university=None)
            university_groups = self.group_by_university(people_group)
            for university, university_group in university_groups.items():
                university_group = self.sort_people(university_group, gender, university)
                self.assign_groups_for_university(university_group, gender, university)
                if len(self.groups) >= self.max_total_groups:
                    break
            if len(self.groups) >= self.max_total_groups:
                break
        return self.groups

    def assign_groups_for_university(self, university_group, gender, university):
        groups_for_person = defaultdict(list)
        for person in university_group:
            if len(groups_for_person[person.name]) < self.max_groups_per_person:
                for group in self.groups:
                    if len(group.members) < self.max_group_size and person not in group.members:
                        if all(undesirable not in group.members for undesirable in person.undesirables):
                            group.add_member(person)
                            groups_for_person[person.name].append(group)
                            break
                if len(groups_for_person[person.name]) >= self.max_groups_per_person:
                    break
                if len(self.groups) >= self.max_total_groups:
                    break
        return self.groups
