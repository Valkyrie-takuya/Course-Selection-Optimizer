# course_selection_optimizer.py
import pulp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class CourseSelectionOptimizer:
    def __init__(self, course_preferences_csv_path, course_capacities_csv_path, min_participants=5):
        self.course_preferences, self.student_genders = self.read_course_preferences(course_preferences_csv_path)
        self.min_participants, self.course_capacities = self.read_course_capacities(course_capacities_csv_path)

    def read_course_preferences(self, csv_path):
        """
        Read the course preferences data from a CSV file.

        Args:
            csv_path (str): The path to the CSV file containing the course preferences data.

        Returns:
            tuple: A tuple containing two dictionaries:
                - course_preferences: A dictionary where the keys are student IDs and the values are dictionaries representing the course preferences for each student.
                - student_genders: A dictionary where the keys are student IDs and the values are the corresponding genders.
        """
        csv_data = pd.read_csv(csv_path)
        course_preferences = {}
        student_genders = {}

        for _, row in csv_data.iterrows():
            student_id = row["4桁番号"]
            student_gender = row["性別"]
            num_preferences = len([col for col in row.index if col.startswith("no")])
            course_preferences[student_id] = {
                row[f"no{i+1}"]: 2 ** i
                for i in range(num_preferences)
            }
            student_genders[student_id] = student_gender

        return course_preferences, student_genders

    def read_course_capacities(self, csv_path):
        """
        Read the course capacities data from a CSV file.

        Args:
            csv_path (str): The path to the CSV file containing the course capacities data.

        Returns:
            tuple: A tuple containing two dictionaries:
                - min_participants: A dictionary where the keys are course names and the values are the minimum number of participants.
                - course_capacities: A dictionary where the keys are course names and the values are the maximum number of participants.
        """
        csv_data = pd.read_csv(csv_path)
        min_participants = {row["講座名"]: row["最少人数"] for _, row in csv_data.iterrows()}
        course_capacities = {row["講座名"]: row["最大人数"] for _, row in csv_data.iterrows()}
        return min_participants, course_capacities

    def convert_values_to_int(self, selected_courses_per_student):
        """
        Convert the selected course IDs from strings to integers.

        Args:
            selected_courses_per_student (dict): A dictionary where the keys are student IDs and the values are the selected course IDs.

        Returns:
            dict: A dictionary where the values are converted to integers.
        """
        converted_dict = {}
        for student_id, course_id in selected_courses_per_student.items():
            converted_course_id = int(course_id[0])
            converted_dict[student_id] = converted_course_id
        return converted_dict

    def save_to_csv(self, selected_courses_per_student, csv_path):
        """
        Save the selected courses per student to a CSV file.

        Args:
            selected_courses_per_student (dict): A dictionary where the keys are student IDs and the values are the selected course IDs.
            csv_path (str): The path to the CSV file to save the data.
        """
        df = pd.DataFrame.from_dict(selected_courses_per_student, orient="index", columns=["講座名"])
        df.index.name = "4桁番号"
        df.to_csv(csv_path, index=True)

    def analyze_hope_and_assignment_data(self, selected_courses_per_student):
        """
        Analyze the fulfilled preference levels for each student.

        Args:
            selected_courses_per_student (dict): A dictionary where the keys are student IDs and the values are the selected course IDs.

        Returns:
            dict: A dictionary where the keys are student IDs and the values are the fulfilled preference levels.
        """
        fulfilled_preference_levels = {}

        for student_id, assigned_course in selected_courses_per_student.items():
            hope_preferences = list(self.course_preferences[student_id].keys())
            fulfilled_preference_index = hope_preferences.index(assigned_course)
            fulfilled_preference_level = fulfilled_preference_index + 1
            fulfilled_preference_levels[student_id] = fulfilled_preference_level

        return fulfilled_preference_levels

    def plot_fulfilled_preference_levels(self, fulfilled_preference_data):
        """
        Plot the distribution of preference fulfilled levels.

        Args:
            fulfilled_preference_data (dict): A dictionary where the keys are student IDs and the values are the fulfilled preference levels.
        """
        num_preference_levels = max(fulfilled_preference_data.values())
        fulfilled_preference_levels = [list(fulfilled_preference_data.values()).count(i) for i in range(1, num_preference_levels + 1)]

        plt.figure(figsize=(8, 6))
        plt.grid(axis="y")
        plt.xticks(np.arange(1, num_preference_levels + 1, 1))
        plt.bar(range(1, num_preference_levels + 1), fulfilled_preference_levels, width=1.0, color="skyblue")
        plt.xlabel("Fulfilled Preference Level")
        plt.ylabel("Number of Students")
        plt.title("Distribution of Fulfilled Preference Levels")
        plt.tight_layout()
        plt.show()

    def decide_courses(self):
        """
        Decide the courses for each student using a linear programming approach.

        Returns:
            dict: A dictionary where the keys are student IDs and the values are the selected course IDs.
        """
        problem = pulp.LpProblem("CourseSelection", pulp.LpMinimize)
        course_selections = pulp.LpVariable.dicts(
            "course_selections",
            ((student, course) for student in self.course_preferences for course in self.course_preferences[student]),
            cat="Binary"
        )

        objective = pulp.lpSum([course_selections[(student, course)] * preference for student, course_prefs in self.course_preferences.items() for course, preference in course_prefs.items()])
        problem += objective

        for student in self.course_preferences:
            problem += pulp.lpSum([course_selections[(student, course)] for course in self.course_preferences[student]]) == 1

        for course in self.course_capacities:
            problem += pulp.lpSum([course_selections[(student, course)] for student in self.course_preferences if course in self.course_preferences[student]]) <= self.course_capacities[course]
            problem += pulp.lpSum([course_selections[(student, course)] for student in self.course_preferences if course in self.course_preferences[student]]) >= self.min_participants[course]

            # Add constraints for gender balance
            num_males = pulp.lpSum([course_selections[(student, course)] for student in self.course_preferences if self.student_genders[student] == "Male"])
            num_females = pulp.lpSum([course_selections[(student, course)] for student in self.course_preferences if self.student_genders[student] == "Female"])
            problem += num_males >= 2  # Require at least one male participant
            problem += num_females >= 2  # Require at least one female participant

        problem.solve()

        selected_courses_per_student = {
            student: [next(course_name for course_name, selection in course_prefs.items() if course_selections[(student, course_name)].value() == 1)]
            for student, course_prefs in self.course_preferences.items()
        }
        selected_courses_per_student = self.convert_values_to_int(selected_courses_per_student)

        return selected_courses_per_student