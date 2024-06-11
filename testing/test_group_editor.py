import unittest
import json
import sys

# setting path
sys.path.append('../groopy')
from group_editor import GroupEditor
from person_editor import PersonEditor

class TestGroupEditor(unittest.TestCase):
    def setUp(self):
        self.person_editor = PersonEditor()
        self.group_editor = GroupEditor(self.person_editor)
        self.person_editor.create_persons_sample()

    def test_load_group(self):
        group_info = {"name": "Group A", "participants": [1, 2, 3]}
        group = self.group_editor.load_group(group_info)
        self.assertEqual(group[0], "Group A")
        self.assertEqual(group[1], [1, 2, 3])

    def test_read_groups_from_json(self):
        with open('test_groups.json', 'w') as file:
            json.dump({
                "groups": {
                    "group1": {"name": "Group A", "participants": [1, 2, 3]},
                    "group2": {"name": "Group B", "participants": [4, 5, 6]}
                }
            }, file)
        groups = self.group_editor.read_groups_from_json('test_groups.json')
        self.assertEqual(len(groups), 2)

    def test_create_groups_from_data(self):
        groups_data = [(1, "Group A", [1, 2, 3]), (2, "Group B", [4, 5, 6])]
        self.group_editor.create_groups_from_data(groups_data)
        self.assertEqual(len(self.group_editor.groups), 2)
        self.assertEqual(self.group_editor.groups[0].name, "Group A")

    def test_move_person_to_group(self):
        self.group_editor.create_groups_from_data([(1, "Group A", [1, 2, 3]), (2, "Group B", [4, 5, 6])])
        result = self.group_editor.move_person_to_group(1, 2)
        self.assertTrue(result)
        group_a = self.group_editor.get_group_by_id(1)
        group_b = self.group_editor.get_group_by_id(2)
        self.assertNotIn(1, [p.id for p in group_a.members])
        self.assertIn(1, [p.id for p in group_b.members])

    def test_find_group_of_person(self):
        self.group_editor.create_groups_from_data([(1, "Group A", [1, 2, 3])])
        group = self.group_editor.find_group_of_person(1)
        self.assertIsNotNone(group)
        self.assertEqual(group.id, 1)

    def test_prep_groups_for_view(self):
        self.group_editor.create_groups_from_data([(1, "Group A", [1, 2, 3])])
        groups_data = self.group_editor.prep_groups_for_view()
        self.assertEqual(len(groups_data), 1)
        self.assertEqual(groups_data[0][0], 1)
        self.assertEqual(groups_data[0][1], "Group A")

    def test_create_group_data_sample(self):
        self.group_editor.create_group_data_sample()
        self.assertEqual(len(self.group_editor.groups), 10)

    def test_print_groups(self):
        self.group_editor.create_group_data_sample()
        self.group_editor.print_groups()
        # This test will visually inspect the printed output

if __name__ == '__main__':
    unittest.main()