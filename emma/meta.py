class HumanMeta:
    def __init__(self):
        """Aggregate all meta information into a dictionary"""
        return {
            "userinfo": self.get_userinfo(),
            "meal_summary": self.get_meal_summary(),
            "exercise_summary": self.get_exercise_summary(),
            "food_preference": self.get_food_preference(),
            "medical_records": self.get_medical_records(),
        }

    def get_userinfo(self):
        """Retrieve user information"""
        pass

    def get_meal_summary(self):
        """Retrieve meal summary"""
        pass

    def get_exercise_summary(self):
        """Retrieve exercise summary"""
        pass

    def get_food_preference(self):
        """Retrieve food preferences"""
        pass

    def get_medical_records(self):
        """Retrieve medical records"""
        pass
