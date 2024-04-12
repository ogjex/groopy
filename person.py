class Person:
    def __init__(self, name, gender, experience, career_preference, desirables, undesirables, university):
        self.name = name
        self.gender = gender
        self.experience = experience
        self.career_preference = career_preference
        self.desirables = desirables
        self.undesirables = undesirables
        self.university = university

    def __str__(self):
        return f"Name: {self.name}, Gender: {self.gender}, University: {self.university}, Experience: {self.experience}, Career Preference: {self.career_preference}"