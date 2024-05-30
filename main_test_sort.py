from grouping_module import GroupingModule
from person import Person
from group import Group

def main():
    # Sample data representing people with their attributes
    people = [
        Person(name="Alice A.", gender="Female", education="Engineering", experience=3, career_preference="Software Development", desirables=["Bob", "Charlie"]),
        Person(name="Bob", gender="Male", education="Software Engineering", experience=5, career_preference="Software Engineering", desirables=["Alice"]),
        Person(name="Charlie", gender="Male", education="Mathematics", experience=2, career_preference="Finance", desirables=["Alice"]),
        Person(name="Eve", gender="Female", education="Engineering", experience=4, career_preference="Software Development", desirables=["Alice", "Bob"]),
        Person(name="Alice B.", gender="Male", education="Engineering", experience=6, career_preference="Data Science", desirables=["Alice"]),
        Person(name="Frank", gender="Male", education="Mathematics", experience=1, career_preference="Software Development"),
        Person(name="Grace", gender="Female", education="Computer Science", experience=4, career_preference="Finance", desirables=["Bob"]),
        Person(name="Harry", gender="Male", education="Engineering", experience=3, career_preference="Data Science", desirables=["Alice"]),
        Person(name="Isabel", gender="Female", education="Mathematics", experience=2, career_preference="Software Development", desirables=["Bob"]),
        Person(name="Jack", gender="Male", education="Engineering", experience=5, career_preference="Finance", desirables=["Alice"]),
        Person(name="Karen", gender="Female", education="Computer Science", experience=3, career_preference="Data Science", desirables=["Alice"]),
        Person(name="Liam", gender="Male", education="Engineering", experience=4, career_preference="Software Development"),
        Person(name="Mia", gender="Female", education="Mathematics", experience=5, career_preference="Data Science", desirables=["Charlie"]),
        Person(name="Nathan", gender="Male", education="Engineering", experience=3, career_preference="Finance", desirables=["Alice"]),
        Person(name="Olivia", gender="Female", education="Computer Science", experience=2, career_preference="Software Development", desirables=["Bob"]),
        Person(name="Peter", gender="Male", education="Mathematics", experience=4, career_preference="Data Science", desirables=["Alice"]),
        Person(name="Quinn", gender="Female", education="Engineering", experience=3, career_preference="Finance", desirables=["Alice"]),
        Person(name="Robert", gender="Male", education="Computer Science", experience=2, career_preference="Software Development", desirables=["Alice"]),
        Person(name="Sophia", gender="Female", education="Mathematics", experience=4, career_preference="Data Science", desirables=["Charlie"]),
        Person(name="Thomas", gender="Male", education="Engineering", experience=5, career_preference="Finance"),
        Person(name="Hortensia", gender="Female", education="Economics", experience=5, career_preference="Finance")
    ]

    # Define parameters
    min_group_size = 3
    max_group_size = 5
    max_groups_per_person = 1
    max_total_groups = 10

    grouping_module = GroupingModule()
    grouping_module.init_group_sort(people, min_group_size, max_group_size, max_groups_per_person, max_total_groups)
    optimal_num_groups = grouping_module.calculate_optimal_num_groups()
    group_list = grouping_module.create_groups(optimal_num_groups)

    # Prompt user for sorting parameters
    num_parameters = int(input("Enter the number of parameters to sort by (1, 2, or 3): "))
    parameters = []
    for i in range(num_parameters):
        parameter = input(f"Enter parameter {i+1}: ")
        parameters.append(parameter)

    sorted_people = people
    for param in parameters:
        param_counts = grouping_module.count_parameter_occurrences(param)
        most_frequent_value = grouping_module.find_most_frequent_parameter_value(param_counts)
        filtered_people = grouping_module.filter_people_by_parameter(sorted_people, param, most_frequent_value)
        remainder_people = grouping_module.find_remainder(sorted_people, filtered_people)

        group_list = grouping_module.distribute_people_to_groups(filtered_people, group_list)
        sorted_people = remainder_people

    group_list = grouping_module.distribute_people_to_groups(sorted_people, group_list)

    # Print groups
    for group in group_list:
        print(group)

if __name__ == "__main__":
    main()
