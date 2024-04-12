class Group:
    def __init__(self, name):
        self.name = name
        self.members = []

    def add_member(self, person):
        self.members.append(person)

def __str__(self):
        member_info = "\n".join([f"{person.name} - {person.university}" for person in self.members])
        return f"Group Members:\n{member_info}"