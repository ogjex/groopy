import json

class WorkspacePreferenceHandler:
    def __init__(self, preference_file="workspace_preferences.json"):
        self.preference_file = preference_file
        self.workspace_title = ""
        self.min_group_size = 1
        self.max_group_size = 1
        self.max_groups_per_person = 1
        self.max_num_groups = 1
        self.persons_list = ""
        self.group_layout = ""
        self.load_preferences()

    def load_preferences(self):
        try:
            with open(self.preference_file, "r") as file:
                data = json.load(file)
                self.workspace_title = data.get("workspace_title", "")
                self.min_group_size = data.get("min_group_size", 1)
                self.max_group_size = data.get("max_group_size", 1)
                self.max_groups_per_person = data.get("max_groups_per_person", 1)
                self.max_num_groups = data.get("max_num_groups", 1)
                self.persons_list = data.get("persons_list", "")
                self.group_layout = data.get("group_layout", "")
        except FileNotFoundError:
            self.save_preferences()  # Save defaults if file not found

    def save_preferences(self):
        data = {
            "workspace_title": self.workspace_title,
            "min_group_size": self.min_group_size,
            "max_group_size": self.max_group_size,
            "max_groups_per_person": self.max_groups_per_person,
            "max_num_groups": self.max_num_groups,
            "persons_list": self.persons_list,
            "group_layout": self.group_layout,
        }
        with open(self.preference_file, "w") as file:
            json.dump(data, file, indent=4)

    # Getters
    def get_workspace_title(self) -> str:
        return self.workspace_title

    def get_min_group_size(self) -> int:
        return self.min_group_size

    def get_max_group_size(self) -> int:
        return self.max_group_size

    def get_max_groups_per_person(self) -> int:
        return self.max_groups_per_person

    def get_max_num_groups(self) -> int:
        return self.max_num_groups

    def get_persons_list(self) -> str:
        return self.persons_list

    def get_group_layout(self) -> str:
        return self.group_layout

    # Setters
    def set_workspace_title(self, title: str):
        self.workspace_title = title
        self.save_preferences()

    def set_min_group_size(self, size: int):
        self.min_group_size = size
        self.save_preferences()

    def set_max_group_size(self, size: int):
        self.max_group_size = size
        self.save_preferences()

    def set_max_groups_per_person(self, num: int):
        self.max_groups_per_person = num
        self.save_preferences()

    def set_max_num_groups(self, num: int):
        self.max_num_groups = num
        self.save_preferences()

    def set_persons_list(self, path: str):
        self.persons_list = path
        self.save_preferences()

    def set_group_layout(self, path: str):
        self.group_layout = path
        self.save_preferences()
