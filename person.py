class Person:
    def __init__(self, name, gender, education, experience, career_preference, desirables=None, undesirables=None):
        self.name = name
        self.gender = gender
        self.education = education
        self.experience = experience
        self.career_preference = career_preference
        self.desirables = desirables if desirables is not None else []
        self.undesirables = undesirables if undesirables is not None else []
        
    def __str__(self):
        return f"Name: {self.name}, Gender: {self.gender}, Education: {self.education}, Experience: {self.experience}, Career Preference: {self.career_preference}"