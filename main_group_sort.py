from group_sorter import GroupSorter
from person_editor import PersonEditor

def main():
    # Initialize PersonEditor to read and manage persons
    person_editor = PersonEditor()
    
    # Read persons from CSV or create sample data
    filename = 'persons.csv'
    people = person_editor.read_persons_from_csv(filename)
    
    # Initialize GroupSorter with parameters
    min_group_size = 3
    max_group_size = 5
    max_groups_per_person = 1
    max_num_groups = 10
    
    # Define sorting and grouping strategies
    #strategies = {'gender': 'focused'}  # Example strategy, can be adjusted
    #strategies = {'gender': 'spread'}
    #strategies = {'gender': 'spread', 'education': 'focused'}
    strategies = {'gender': 'focused', 'education': 'spread'}
    
    # Create an instance of GroupSorter
    sorter = GroupSorter(min_group_size, max_group_size, max_groups_per_person, max_num_groups)
    
    # Set the people to be sorted
    sorter.set_people_to_sort(people)
    
    # Sort people based on parameters if strategy is 'focused'
    if any(strategy == 'focused' for strategy in strategies.values()):
        sorted_people = sorter.sort_people_by_parameters(list(strategies.keys()))
    else:
        sorted_people = people  # No sorting if strategy is 'spread'
    
    # Distribute people into groups based on strategies
    groups = sorter.distribute_people_to_groups(sorted_people, strategies)
    
    # Print out the groups
    for group in groups:
        print(f"Group {group.id} ({len(group.members)} members):")
        for person in group.members:
            print(f"- {person.id}, {person.name}, {person.gender}, {person.education}")
        print()

if __name__ == "__main__":
    main()