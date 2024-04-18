import pulp
import pandas as pd
import matplotlib.pyplot as plt

def read_course_preferences(csv_path):
    # Read CSV data
    csv_data = pd.read_csv(csv_path)
    course_preferences = {}
    print(csv_data)
    for index, row in csv_data.iterrows():
        student_id = row["4桁番号"]
        course_preferences[student_id] = {
            row["no1"]: 8,
            row["no2"]: 4,
            row["no3"]: 2,
            row["no4"]: 1,
        }
    return course_preferences

def read_course_capacities(csv_path):
    # Read CSV data
    csv_data = pd.read_csv(csv_path)
    course_capacities = {}

    for index, row in csv_data.iterrows():
        student_id = row["講座名"]
        course_capacities[student_id] = row["人数"]
    return course_capacities

def save_to_csv(selected_courses_per_student, csv_path):
    df = pd.DataFrame.from_dict(selected_courses_per_student, orient="index", columns=["4桁番号", "講座名"])
    df.to_csv(csv_path, index=True)

def analyze_hope_and_assignment_data(course_preferences, selected_courses_per_student):
    fulfilled_preference_levels = {}

    for student_id, assigned_course in selected_courses_per_student.items():
        hope_preferences = list(course_preferences[student_id].keys())

        fulfilled_preference_index = hope_preferences.index(assigned_course[0])
        fulfilled_preference_level = fulfilled_preference_index + 1

        fulfilled_preference_levels[student_id] = fulfilled_preference_level

    return fulfilled_preference_levels

def plot_fulfilled_preference_levels(fulfilled_preference_data):
    # Extract fulfilled preference levels from the dictionary
    fulfilled_preference_levels = list(fulfilled_preference_data.values())

    # Create a bar chart
    plt.figure(figsize=(8, 6))
    _fulfilled_preference_levels = []

    for i in range(1,6):
        _fulfilled_preference_levels.append(fulfilled_preference_levels.count(i))

    plt.bar(range(1,6), _fulfilled_preference_levels, width=1.0, color="skyblue")
    plt.xlabel("Fulfilled Preference Level")
    plt.ylabel("Number of Students")
    plt.title("Distribution of Fulfilled Preference Levels")

    # Show the chart
    plt.tight_layout()
    plt.show()

def decide_courses(course_preferences, course_capacities):
    # Define the problem
    problem = pulp.LpProblem("CourseSelection", pulp.LpMaximize)

    # Variables: course_selections[(student, course)] == 1 if the student selects the course
    course_selections = pulp.LpVariable.dicts(
        "course_selections",
        ((student, course) for student in course_preferences for course in course_preferences[student]),
        cat="Binary"
    )

    # Objective: Maximize the total preference of the students
    objective = pulp.lpSum([course_selections[(student, course)] * preference for student, course_prefs in course_preferences.items() for course, preference in course_prefs.items()])
    problem += objective

    # Constraints: Each student selects one course
    for student in course_preferences:
        problem += pulp.lpSum([course_selections[(student, course)] for course in course_preferences[student]]) == 1

    # Constraints: The number of students selecting each course does not exceed its capacity
    for course in course_capacities:
        problem += pulp.lpSum([course_selections[(student, course)] for student in course_preferences if course in course_preferences[student]]) <= course_capacities[course]

    # Solve the problem
    problem.solve()

    # Get the selected courses for each student
    selected_courses_per_student = {}
    for student, course_prefs in course_preferences.items():
        selected_courses = []
        for course_name, preference in course_prefs.items():
            if course_selections[(student, course_name)].value() == 1:
                selected_courses.append(course_name)
        selected_courses_per_student[student] = selected_courses

    return selected_courses_per_student


def main():
    course_preferences_csv_path = "course_preferences.csv"
    course_preferences = read_course_preferences(course_preferences_csv_path)
    print(len(course_preferences))
    print(course_preferences)

    course_capacities_csv_path = "course_capacities.csv"
    course_capacities = read_course_capacities(course_capacities_csv_path)
    print(course_capacities)

    selected_courses_per_student = decide_courses(course_preferences, course_capacities)
    print(selected_courses_per_student)

    export_path = "selected_courses.csv"
    save_to_csv(selected_courses_per_student, export_path)
    
    fulfilled_preference_levels = analyze_hope_and_assignment_data(course_preferences, selected_courses_per_student)
    print(fulfilled_preference_levels)

    plot_fulfilled_preference_levels(fulfilled_preference_levels)


if __name__ == "__main__":
    main()