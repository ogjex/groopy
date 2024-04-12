from collections import defaultdict
from person import Person
from group import Group
import itertools
class GroupingModule:
    def __init__(self, people, min_group_size, max_group_size, max_groups_per_person):
        self.people = people
        self.min_group_size = min_group_size
        self.max_group_size = max_group_size
        self.max_groups_per_person = max_groups_per_person
        self.groups = []

    def group_by_gender(self):
        gender_groups = defaultdict(list)
        for person in self.people:
            gender_groups[person.gender].append(person)
        return gender_groups

    def sort_by_experience(self, people):
        return sorted(people, key=lambda x: x.experience, reverse=True)

    def sort_by_career_preference(self, people):
        return sorted(people, key=lambda x: x.career_preference)

    def sort_by_desirables(self, people):
        return sorted(people, key=lambda x: len(x.desirables) if x.desirables else -1)

    def sort_by_undesirables(self, people):
        return sorted(people, key=lambda x: len(x.undesirables), reverse=True)

    def assign_groups(self):
        gender_groups = self.group_by_gender()
        for gender, people_group in gender_groups.items():
            people_group = self.sort_by_experience(people_group)
            people_group = self.sort_by_career_preference(people_group)
            people_group = self.sort_by_desirables(people_group)
            people_group = self.sort_by_undesirables(people_group)
            university_groups = defaultdict(list)
            for person in people_group:
                university_groups[person.university].append(person)
            for university, university_group in university_groups.items():
                university_group = self.sort_by_experience(university_group)
                university_group = self.sort_by_career_preference(university_group)
                university_group = self.sort_by_desirables(university_group)
                university_group = self.sort_by_undesirables(university_group)
                group_name = f"{gender} - {university}"
                groups_for_person = defaultdict(list)
                for person in university_group:
                    if len(groups_for_person[person.name]) < self.max_groups_per_person:
                        for group in self.groups:
                            if len(group.members) < self.max_group_size and person not in group.members:
                                if len(group.members) < self.min_group_size or len(group.members) == self.max_group_size - 1:
                                    group.add_member(person)
                                    groups_for_person[person.name].append(group)
                                    break
                                else:
                                    combinations = list(itertools.combinations(group.members, 2))
                                    if all(person in combo for combo in combinations):
                                        group.add_member(person)
                                        groups_for_person[person.name].append(group)
                                        break
                                    elif any(person in combo for combo in combinations):
                                        group.add_member(person)
                                        groups_for_person[person.name].append(group)
                                        break
                    if len(groups_for_person[person.name]) >= self.max_groups_per_person:
                        break
                    if len(self.groups) >= len(self.people) / self.max_group_size:
                        break
                for person, groups in groups_for_person.items():
                    if len(groups) < self.max_groups_per_person:
                        for group in self.groups:
                            if len(group.members) < self.max_group_size and person not in group.members:
                                group.add_member(person)
                                groups_for_person[person.name].append(group)
                                break
        return self.groups