import unittest
import os
from workspace_preference_handler import WorkspacePreferenceHandler

class TestWorkspacePreferenceHandler(unittest.TestCase):
    def setUp(self):
        self.preference_file = "test_workspace_preferences.json"
        self.handler = WorkspacePreferenceHandler(preference_file=self.preference_file)

    def tearDown(self):
        if os.path.exists(self.preference_file):
            os.remove(self.preference_file)

    def test_initialization(self):
        self.assertTrue(os.path.exists(self.preference_file))
        self.assertEqual(self.handler.get_workspace_title(), "")
        self.assertEqual(self.handler.get_min_group_size(), 1)
        self.assertEqual(self.handler.get_max_group_size(), 1)
        self.assertEqual(self.handler.get_max_groups_per_person(), 1)
        self.assertEqual(self.handler.get_max_num_groups(), 1)
        self.assertEqual(self.handler.get_persons_list(), "")
        self.assertEqual(self.handler.get_group_layout(), "")

    def test_set_and_get_methods(self):
        self.handler.set_workspace_title("Test Workspace")
        self.handler.set_min_group_size(5)
        self.handler.set_max_group_size(10)
        self.handler.set_max_groups_per_person(3)
        self.handler.set_max_num_groups(20)
        self.handler.set_persons_list("test_persons.json")
        self.handler.set_group_layout("test_layout.json")

        self.assertEqual(self.handler.get_workspace_title(), "Test Workspace")
        self.assertEqual(self.handler.get_min_group_size(), 5)
        self.assertEqual(self.handler.get_max_group_size(), 10)
        self.assertEqual(self.handler.get_max_groups_per_person(), 3)
        self.assertEqual(self.handler.get_max_num_groups(), 20)
        self.assertEqual(self.handler.get_persons_list(), "test_persons.json")
        self.assertEqual(self.handler.get_group_layout(), "test_layout.json")

    def test_save_and_load_preferences(self):
        self.handler.set_workspace_title("Test Workspace")
        self.handler.set_min_group_size(5)
        self.handler.set_max_group_size(10)
        self.handler.set_max_groups_per_person(3)
        self.handler.set_max_num_groups(20)
        self.handler.set_persons_list("test_persons.json")
        self.handler.set_group_layout("test_layout.json")
        self.handler.save_preferences()

        # Create a new handler to load preferences
        new_handler = WorkspacePreferenceHandler(preference_file=self.preference_file)

        # Check if loaded preferences match
        self.assertEqual(new_handler.get_workspace_title(), "Test Workspace")
        self.assertEqual(new_handler.get_min_group_size(), 5)
        self.assertEqual(new_handler.get_max_group_size(), 10)
        self.assertEqual(new_handler.get_max_groups_per_person(), 3)
        self.assertEqual(new_handler.get_max_num_groups(), 20)
        self.assertEqual(new_handler.get_persons_list(), "test_persons.json")
        self.assertEqual(new_handler.get_group_layout(), "test_layout.json")

if __name__ == "__main__":
    unittest.main()
