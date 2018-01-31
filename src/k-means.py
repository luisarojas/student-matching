# ------------------------ ARGS SET-UP ------------------------
import argparse

# set-up command-line arguments
parser = argparse.ArgumentParser(description="Run k-means clustering on mentors and first-year students.")
parser._action_groups.pop()

required_args = parser.add_argument_group('required named arguments')

# add command-line argument flags and options
required_args.add_argument('-m', '--mentorinput', help="Provide the path for the INPUT file for all MENTORS (.xlsx) sheet.", required=True)
required_args.add_argument('-s', '--studentinput', help="Provide the path for the INPUT file for all STUDENTS (.xlsx) sheet.", required=True)
args = parser.parse_args()

# ------------------------ SET VARIABLES AND CONSTANTS ------------------------

MAX_CLUSTERS = 100

# assign arguments to variables
mentor_input_file = args.mentorinput;
student_input_file = args.studentinput;

# ------------------------ IMPLEMENTATION ------------------------
import pandas as pd

# load spreadsheets
xl_mentors = pd.ExcelFile(mentor_input_file)
xl_students = pd.ExcelFile(student_input_file)

# load the first sheet into a DataFrame by name: df
df_mentors = xl_mentors.parse(xl_mentors.sheet_names[0])
df_students = xl_students.parse(xl_students.sheet_names[0])

# insert new column 'is_mentor'
df_mentors = df_mentors.assign(is_mentor='True')
df_students = df_students.assign(is_mentor='False')

# merge both dataframes vertically
df = pd.concat([df_mentors, df_students])

# TODO UNDER CONSTRUCTION!
