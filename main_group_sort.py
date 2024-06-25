from group_sorter import GroupSorter
from person import Person
from person_editor import PersonEditor
from group import Group

def main():
    my_person_editor = PersonEditor()
    people = my_person_editor.create_persons_sample()

    # Define parameters
    min_group_size = 3
    max_group_size = 5
    max_groups_per_person = 1
    max_total_groups = 10


    # Create an instance of GroupSorter
    grouping_module = GroupSorter(
        min_group_size=min_group_size,
        max_group_size=max_group_size,
        max_groups_per_person=max_groups_per_person,
        max_num_groups=max_total_groups
    )

    # Set the people to the GroupSorter
    grouping_module.set_people_to_sort(people)

    # Define sorting parameters and strategies
    sorting_parameters = ['gender', 'education']
    strategies = {'gender': 'homogeneous', 'education': 'heterogeneous'}
    #strategies = {'gender': 'heterogeneous'}
    #strategies = {'gender': 'homogeneous'}

    # Sort people based on the parameters
    sorted_people = grouping_module.sort_people_by_parameters(sorting_parameters)

    # Distribute sorted people into groups based on the strategies
    groups = grouping_module.distribute_people_to_groups(sorted_people, strategies)

    # Print the groups and their members for verification
    for group in groups:
        print(f"\n{group.name} (ID: {group.id}):")
        for member in group.members:
            print(f"- {member.id}, {member.name}, {member.gender}, {member.education}")

if __name__ == "__main__":
    main()