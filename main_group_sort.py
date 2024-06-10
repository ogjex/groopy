from group_sorter import GroupingModule
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

    grouping_module = GroupingModule()
    # following sorts by 1 parameter
    '''grouping_module.init_group_sort(people, min_group_size, max_group_size, max_groups_per_person, max_total_groups)
    optimal_num_groups = grouping_module.calculate_optimal_num_groups()
    
    target_parameter = 'gender'
    parameter_counts = grouping_module.count_parameter_occurrences(target_parameter)
    most_frequent_parameter_value = grouping_module.find_most_frequent_parameter_value(parameter_counts)
    
    filtered_people_list = grouping_module.filter_people_by_parameter(target_parameter, most_frequent_parameter_value)
    remainder_list = grouping_module.find_remainder(people, filtered_people_list)
    
    group_list = grouping_module.create_groups(optimal_num_groups)
    
    group_list = grouping_module.distribute_people_to_groups(filtered_people_list, group_list)
    
    #second_target_parameter = 'education'
    #parameter_counts = grouping_module.count_parameter_occurrences(second_target_parameter)
    #most_frequent_parameter_value = grouping_module.find_most_frequent_parameter_value(second_target_parameter)

    group_list = grouping_module.distribute_people_to_groups(remainder_list, group_list)'''

    # following sorts by 2 parameters
    grouping_module.init_group_sort(people, min_group_size, max_group_size, max_groups_per_person, max_total_groups)
    optimal_num_groups = grouping_module.calculate_optimal_num_groups()
    
    #create empty group list
    group_list = grouping_module.create_groups(optimal_num_groups)

    target_parameter = 'gender'
    parameter_counts = grouping_module.count_parameter_occurrences(target_parameter)
    most_frequent_parameter_value = grouping_module.find_most_frequent_parameter_value(parameter_counts)
    
    A_filtered_people = grouping_module.filter_people_by_parameter(people, target_parameter, most_frequent_parameter_value)
    B_remainder_people = grouping_module.find_remainder(people, A_filtered_people)


    # find the parameter value that is most frequent to sort both lists from
    second_target_parameter = 'education'
    parameter_counts = grouping_module.count_parameter_occurrences(second_target_parameter)    
    most_frequent_second_target_parameter_value = grouping_module.find_most_frequent_parameter_value(parameter_counts)
    
    A1_filtered_people = grouping_module.filter_people_by_parameter(A_filtered_people, second_target_parameter, most_frequent_second_target_parameter_value)
    A2_remainder_people = grouping_module.find_remainder(A_filtered_people, A1_filtered_people)

    B1_filtered_people = grouping_module.filter_people_by_parameter(B_remainder_people, second_target_parameter, most_frequent_second_target_parameter_value)
    B2_remainder_people = grouping_module.find_remainder(B_remainder_people, B1_filtered_people)

    group_list = grouping_module.distribute_people_to_groups(A1_filtered_people, group_list)
    group_list = grouping_module.distribute_people_to_groups(B1_filtered_people, group_list)
    group_list = grouping_module.distribute_people_to_groups(A2_remainder_people, group_list)
    group_list = grouping_module.distribute_people_to_groups(B2_remainder_people, group_list)
    

    # Print groups    
    for group in group_list:
        print(group)

if __name__ == "__main__":
    main()
