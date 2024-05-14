import unittest
import json
from group_editor import GroupEditor

class TestGroupEditor(unittest.TestCase):
    def setUp(self):
        self.editor = GroupEditor()

    def test_get_group_names_empty(self):
        self.assertEqual(self.editor.get_group_names(), [])

    def test_get_group_names(self):
        self.editor.groups = [
            Group("Group 1", ["Alice", "Bob"]),
            Group("Group 2", ["Charlie", "David"])
        ]
        self.assertEqual(self.editor.get_group_names(), ["Group 1", "Group 2"])

    def test_load_groups_from_json(self):
        json_data = '''
        {
            "number_of_groups": 2,
            "groups": {
                "group1": {
                    "name": "Group 1",
                    "participants": ["Alice", "Bob"]
                },
                "group2": {
                    "name": "Group 2",
                    "participants": ["Charlie", "David"]
                }
            }
        }
        '''
        with open("test_groups.json", 'w') as json_file:
            json_file.write(json_data)

        groups = self.editor.read_groups_from_json("test_groups.json")
        self.assertEqual(groups, [("Group 1", ["Alice", "Bob"]), ("Group 2", ["Charlie", "David"])])

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
