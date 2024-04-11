from grouping_module import GroupingModule
from person import Person

def main():
    # Sample data representing people with their attributes
    people = [
        Person("Alice", "Female", 3, "Engineering", ["Bob", "Charlie"], ["David", "Eve"], "Harvard"),
        Person("Bob", "Male", 2, "Engineering", ["Alice", "David"], ["Eve"], "MIT"),
        Person("Charlie", "Male", 1, "Marketing", ["Alice", "Eve"], ["David"], "Stanford"),
        Person("David", "Male", 3, "Marketing", ["Bob", "Alice"], ["Charlie"], "Stanford"),
        Person("Eve", "Female", 2, "Engineering", ["Charlie", "Alice"], ["Bob"], "MIT")
    ]

    # Define parameters
    min_group_size = 3
    max_group_size = 5
    max_groups_per_person = 2

    grouping_module = GroupingModule(people, min_group_size, max_group_size, max_groups_per_person)
    grouping_module.assign_groups()

    # Print groups
    for i, group in enumerate(grouping_module.groups):
        print(f"Group {i + 1} ({group.name}):")
        for member in group.members:
            print(f"  {member.name} - {member.gender} - Experience: {member.experience} - Career Preference: {member.career_preference} - Desirables: {member.desirables} - Undesirables: {member.undesirables} - University: {member.university}")

if __name__ == "__main__":
    main()
