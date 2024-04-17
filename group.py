class Group:
    def __init__(self, name:str):
        self.name = name
        self.members = []
        self.gender_is_balanced = False
        self.university_is_diverse = False

    def add_member(self, person):
        self.members.append(person)

    def calculate_gender_balance(self, gender_threshold=0.4):
        if not self.members:
            return False

        # Count the number of males and females in the group
        num_males = sum(1 for person in self.members if person.gender == 'Male')
        num_females = sum(1 for person in self.members if person.gender == 'Female')

        # Check gender balance
        gender_balance = min(num_males, num_females) / len(self.members)
        self.gender_is_balanced = gender_balance >= gender_threshold
        return self.gender_is_balanced

    def calculate_education_diversity(self, education_threshold=0.5):
        if not self.members:
            return False

        # Count the number of unique universities in the group
        educations = set(person.education for person in self.members)

        # Check university diversity
        education_diversity = len(educations) / len(self.members)
        self.university_is_diverse = education_diversity >= education_diversity
        return self.university_is_diverse

    def __str__(self):
        member_info = "\n".join([f"{person.name} - {person.education}" for person in self.members])
        return f"Group Members:\n{member_info}"