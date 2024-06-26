class Person:
    def __init__(self, id, name, gender, education, experience, career_preference, desirables=None, undesirables=None):
        self.id = id
        self.name = name
        self.gender = gender
        self.education = education
        self.experience = experience
        self.career_preference = career_preference
        self.desirables = desirables if desirables is not None else []
        self.undesirables = undesirables if undesirables is not None else []
        
    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, Gender: {self.gender}, Education: {self.education}, Experience: {self.experience}, Career Preference: {self.career_preference}"

    def __eq__(self, other):
        return (self.name, self.gender, self.education, self.experience, self.career_preference) == \
               (other.name, other.gender, other.education, other.experience, other.career_preference)

    def __hash__(self):
        return hash((self.name, self.gender, self.education, self.experience, self.career_preference))