import random
import string
import pandas as pd


def generate_course_preferences(num_students, num_courses):
    """Generates random course preferences for students.

    Args:
        num_students (int): Number of students.
        num_courses (int): Number of available courses.

    Returns:
        dict: Dictionary containing student IDs as keys and course preferences as lists.
    """

    # Generate 4-digit student IDs
    student_ids = ["".join(random.choice(string.digits) for _ in range(4)) for _ in range(num_students)]

    course_preferences = {}
    for student_id in student_ids:
        # Generate random course preferences (order matters)
        preferences = random.sample(range(1, num_courses + 1), num_courses)
        course_preferences[student_id] = preferences

    return course_preferences


def generate_course_capacities(courses):
    """Generates random capacities for each course.

    Args:
        courses (list): List of course names/identifiers.

    Returns:
        dict: Dictionary containing courses as keys and capacities as values.
    """

    course_capacities = {}
    for course in courses:
        course_capacities[course] = random.randint(1, 20)  # Adjust capacity range as needed

    return course_capacities


def generate_predicted_output(course_preferences, course_capacities):
    """Generates a dictionary representing predicted course assignments.

    Args:
        course_preferences (dict): Dictionary containing student IDs and course preferences.
        course_capacities (dict): Dictionary containing courses and their capacities.

    Returns:
        dict: Dictionary containing student IDs as keys and assigned courses (with counts) as values.
    """

    predicted_assignments = {}
    for student_id, preferences in course_preferences.items():
        assigned_course = None

        # Assign the most preferred course within the available capacity
        for course in preferences:
            course_name = str(course)  # Convert course number to string
            if course_capacities[course_name] > 0:
                assigned_course = course_name
                course_capacities[course_name] -= 1
                break

        # If no course could be assigned, mark as unassigned
        if not assigned_course:
            assigned_course = "Unassigned"

        predicted_assignments[student_id] = {assigned_course: 1}

    return predicted_assignments


def main():
    """Generates and processes course preference and capacity data."""

    # Define number of courses
    num_courses = 16  # Adjust the number of courses as needed

    # Generate test data
    num_students = 250  # Adjust the number of students as needed

    course_preferences = generate_course_preferences(num_students, num_courses)

    # Generate course names/identifiers automatically based on number of courses
    course_options = [str(i) for i in range(1, num_courses + 1)]

    # Create DataFrame with automatic column names
    df = pd.DataFrame.from_dict(course_preferences, orient="index")
    df.columns = [f"no{i}" for i in range(1, num_courses + 1)]  # Dynamic column names
    df.index.name = "4桁番号"
    df.to_csv("course_preferences.csv", index=True)

    course_capacities = generate_course_capacities(course_options)
    df = pd.DataFrame.from_dict(course_capacities, orient="index", columns=["人数"])
    df.index.name = "講座名"
    df.to_csv("course_capacities.csv", index=True)

    predicted_output = generate_predicted_output(course_preferences, course_capacities)
    print(predicted_output)


if __name__ == "__main__":
    main()
