import sys
import unittest
# setting path
sys.path.append('../groopy')
from grouping_module import GroupingModule
from person import Person
from group import Group

class TestGroupingModule(unittest.TestCase):
    def setUp(self):
        # Initialize test data
        self.people1 = [
            Person(name="Alice", gender="Female", education="Engineering", experience=3, career_preference="Software Development", desirables=["Bob", "Charlie"]),
            Person(name="Bob", gender="Male", education="Software Engineering", experience=5, career_preference="Software Engineering", desirables=["Alice"]),
            Person(name="Charlie", gender="Male", education="Mathematics", experience=2, career_preference="Finance", desirables=["Alice"]),
            Person(name="Eve", gender="Female", education="Engineering", experience=4, career_preference="Software Development", desirables=["Alice", "Bob"]),
            Person(name="Alice", gender="Male", education="Engineering", experience=6, career_preference="Data Science", desirables=["Alice"]),
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

        ''' people2 = [
            Person(name="Person 1", education="Engineering"),
            Person(name="Person 2", education="Computer Science"),
            Person(name="Person 3", education="Engineering"),
            Person(name="Person 4", education="Mathematics"),
            Person(name="Person 5", education="Computer Science"),
            Person(name="Person 6", education="Mathematics"),
            Person(name="Person 7", education="Engineering"),
            Person(name="Person 8", education="Mathematics"),
            Person(name="Person 9", education="Computer Science"),
            Person(name="Person 10", education="Engineering")
        ]'''
        #self.people = people1
        self.min_group_size = 3
        self.max_group_size = 5
        self.max_groups_per_person = 1
        self.max_total_groups = 10
        self.test_grouping_module = GroupingModule(self.people1, self.min_group_size, self.max_group_size, self.max_groups_per_person, self.max_total_groups)   
        
    def test_count_parameter_occurrences(self):
        # Create a list of Person objects for testing
        people_list = [
            Person("John", "Male", "Engineering", 5, "Software Developer", ["Alice", "Bob"], ["Carol"]),
            Person("Alice", "Female", "Science", 4, "Data Analyst", ["John"], ["Bob"]),
            Person("Bob", "Male", "Engineering", 3, "Web Developer", ["John"], ["Alice"]),
            Person("Carol", "Female", "Science", 6, "Research Scientist", ["David"], ["John"]),
            Person("David", "Male", "Engineering", 7, "Data Scientist", ["Carol"], ["Alice"])
        ]

        # Test counting occurrences of gender
        gender_counts = self.test_grouping_module.count_parameter_occurrences(people_list, "gender")
        self.assertEqual(gender_counts, {"Male": 3, "Female": 2})

        # Test counting occurrences of education
        education_counts = self.test_grouping_module.count_parameter_occurrences(people_list, "education")
        self.assertEqual(education_counts, {"Engineering": 3, "Science": 2})

    def test_find_most_frequent_parameter_value(self):
        # Create a parameter counts dictionary for testing
        parameter_counts = {"Male": 3, "Female": 2}

        # Test finding the most frequent parameter value
        most_frequent_gender = self.test_grouping_module.find_most_frequent_parameter_value(parameter_counts)
        self.assertEqual(most_frequent_gender, "Male")

        # Update the parameter counts for testing
        parameter_counts = {"Engineering": 3, "Science": 2}

        # Test finding the most frequent parameter value
        most_frequent_education = self.test_grouping_module.find_most_frequent_parameter_value(parameter_counts)
        self.assertEqual(most_frequent_education, "Engineering")

    def test_calculate_optimal_num_groups_exact_multiple(self):
        # Test when total_people is an exact multiple of max_group_size
        gm = GroupingModule(people=[], min_group_size=3, max_group_size=6, max_groups_per_person=2, max_total_groups=10)
        result = gm.calculate_optimal_num_groups(total_people=18, min_group_size=3, max_group_size=6, max_num_groups=10)
        self.assertEqual(result, 3)  # 18 people can be divided into 3 groups of 6 each

    def test_calculate_optimal_num_groups_not_exact_multiple(self):
        # Test when total_people is not an exact multiple of max_group_size
        gm = GroupingModule(people=[], min_group_size=3, max_group_size=6, max_groups_per_person=2, max_total_groups=10)
        result = gm.calculate_optimal_num_groups(total_people=19, min_group_size=3, max_group_size=6, max_num_groups=10)
        self.assertEqual(result, 4)  # 19 people can be divided into 4 groups (3 groups of 6 and 1 group of 1)

    def test_calculate_optimal_num_groups_max_num_groups_limit(self):
        # Test when max_num_groups is smaller than the maximum possible number of groups
        gm = GroupingModule(people=[], min_group_size=3, max_group_size=6, max_groups_per_person=2, max_total_groups=10)
        result = gm.calculate_optimal_num_groups(total_people=20, min_group_size=3, max_group_size=6, max_num_groups=2)
        self.assertEqual(result, 2)  # Only 2 groups allowed, even though more are possible

    def test_create_groups(self):
        groups_to_create = 5
        created_groups = self.test_grouping_module.create_groups(groups_to_create)

        # Check if the number of created groups matches the specified input parameter
        self.assertEqual(len(created_groups), groups_to_create)

        # Check if each element in the created_groups list is an instance of the Group class
        for group in created_groups:
            self.assertIsInstance(group, Group)
    
    def test_filter_by_education(self):
        gm = GroupingModule(self.people1, min_group_size=3, max_group_size=6, max_groups_per_person=2, max_total_groups=10)
        filtered_people = gm.filter_people_by_parameter(self.people1, parameter="education", value="Software Engineering")
        self.assertEqual(len(filtered_people), 1)  # Only Bob is a software engineer
        self.assertEqual(filtered_people[0].name, "Bob")

    def test_filter_by_experience(self):
        gm = GroupingModule(self.people1, min_group_size=3, max_group_size=6, max_groups_per_person=2, max_total_groups=10)
        filtered_people = gm.filter_people_by_parameter(self.people1, parameter="experience", value=6)
        self.assertEqual(len(filtered_people), 1)  # Only Alice has 6 years of experience
        self.assertEqual(filtered_people[0].name, "Alice")

    def test_find_remainder(self):        
        # Define two lists of Person objects
        self.person1 = Person("Alice", "Female", "Masters", "5 years", "Engineering")
        self.person2 = Person("Bob", "Male", "Bachelor", "3 years", "Finance")
        self.person3 = Person("Charlie", "Male", "PhD", "10 years", "Research")
        self.person4 = Person("Diana", "Female", "Masters", "8 years", "Marketing")

        list1 = [self.person1, self.person2, self.person3]
        list2 = [self.person2, self.person3, self.person4]

        # Call the find_remainder method
        remainder = self.test_grouping_module.find_remainder(list1, list2)
        
        # Assert that the length of the remainder list is 2 (person1 and person4)
        self.assertEqual(len(remainder), 2)
        
        # Assert that person1 and person4 are in the remainder list
        self.assertIn(self.person1, remainder)
        self.assertIn(self.person4, remainder)

    def test_distribute_people_to_groups(self):
        self.person1 = Person("Alice", "Female", "Masters", "5 years", "Engineering")
        self.person2 = Person("Bob", "Male", "Bachelor", "3 years", "Finance")
        self.person3 = Person("Charlie", "Male", "PhD", "10 years", "Research")
        self.person4 = Person("Diana", "Female", "Masters", "8 years", "Marketing")
        self.person5 = Person("Diana", "Female", "Masters", "8 years", "Marketing")
        self.person6 = Person("Diana", "Female", "Masters", "8 years", "Marketing")
        self.person7 = Person("Diana", "Female", "Masters", "8 years", "Marketing")
        self.person8 = Person("John", "Female", "Masters", "8 years", "Marketing")

        # Create some sample Group objects for testing
        self.group1 = Group("Group 1")
        self.group2 = Group("Group 2")
        self.group3 = Group("Group 3")
        # Create an instance of GroupingModule

        grouping_module = GroupingModule([], 2, 5, 3, 10)

        # Define a list of people and groups
        people_list = self.people1#[self.person1, self.person2, self.person3, self.person4]
        group_list = [self.group1, self.group2, self.group3]

        # Call the distribute_people_to_groups method
        updated_group_list = grouping_module.distribute_people_to_groups(people_list, group_list)

        # Print out the participants in each group for verification
        for group in updated_group_list:
            print(f"Participants in {group.name}:")
            for person in group.members:
                print(person.name)

if __name__ == '__main__':
        unittest.main()