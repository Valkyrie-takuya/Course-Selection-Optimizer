# app.py
import os
import tkinter as tk
from tkinter import filedialog
from course_selection_optimizer import CourseSelectionOptimizer

def get_file_paths():
    """
    Open a file dialog to select the course preferences and course capacities CSV files.

    Returns:
        tuple: The paths to the course preferences and course capacities CSV files.
    """
    root = tk.Tk()
    root.withdraw()
    root.lift()

    course_preferences_csv_path = filedialog.askopenfilename(filetypes=[("データファイル","*.csv")], title="Select Course Preferences CSV File")
    course_capacities_csv_path = filedialog.askopenfilename(filetypes=[("データファイル","*.csv")], title="Select Course Capacities CSV File")

    return course_preferences_csv_path, course_capacities_csv_path

def main():
    """
    The main function that orchestrates the course selection optimization process.
    """
    course_preferences_csv_path, course_capacities_csv_path = get_file_paths()
    optimizer = CourseSelectionOptimizer(course_preferences_csv_path, course_capacities_csv_path)
    selected_courses_per_student = optimizer.decide_courses()

    # Create an "output" directory if it doesn't exist
    if not os.path.isdir("output"):
        os.mkdir("output")
    export_path = "output/selected_courses.csv"
    optimizer.save_to_csv(selected_courses_per_student, export_path)

    fulfilled_preference_levels = optimizer.analyze_hope_and_assignment_data(selected_courses_per_student)
    optimizer.plot_fulfilled_preference_levels(fulfilled_preference_levels)

if __name__ == "__main__":
    main()