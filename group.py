class Group:
    def __init__(self, name):
        self.name = name
        self.members = []

    def add_member(self, person):
        self.members.append(person)

    def __str__(self):
        return ', '.join(str(member) for member in self.members)