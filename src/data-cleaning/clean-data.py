import argparse

# set-up command-line arguments
parser = argparse.ArgumentParser(description="Clean mentors and students data.")
parser._action_groups.pop()

required_args = parser.add_argument_group('required named arguments')
optional_args = parser.add_argument_group('optional named arguments')

# add command-line argument flags and options
required_args.add_argument('-m', '--mentorinput', help="Provide the path for the INPUT file for all MENTORS (.xlsx) sheet.", required=True)
required_args.add_argument('-s', '--studentinput', help="Provide the path for the INPUT file for all STUDENTS (.xlsx) sheet.", required=True)
optional_args.add_argument('-mo', '--mentoroutput', help="Provide the path for the OUTPUT file for all MENTORS (.xlsx) sheet (default='mentors-clean.xlsx').", default="../../data/mentors-clean.xlsx")
optional_args.add_argument('-so', '--studentoutput', help="Provide the path for the OUTPUT file for all STUDENTS (.xlsx) sheet (default='students-clean.xlsx').", default="../../data/students-clean.xlsx")
args = parser.parse_args()

# assign arguments to variables
mentor_input_file = args.mentorinput;
student_input_file = args.studentinput;
mentor_output_file = args.mentoroutput;
student_output_file = args.studentoutput;

import pandas as pd
import re

def clean_files(input_file, output_file):

    print('> Saving to file ' + output_file)

    # load spreadsheet
    xl = pd.ExcelFile(input_file)

    # load the first sheet into a DataFrame by name: df
    df = xl.parse(xl.sheet_names[0])
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace('\s', '_')  # in case there are multiple white spaces

    # clean up multiple answers for yes/no/not applicable questions
    for i, header in enumerate(df[:][4:]):
        curr_col = df[header]

        for j, elem in enumerate(curr_col):

            if (re.match("(.+);(Not Applicable)", str(elem))):
                curr_col = df[header][j] = 'Not Applicable'

            elif (re.match("(Yes);(No)", str(elem))):
                curr_col = df[header][j] = 'No'

            else:
                pass

    # replace all 'Health Science' instances under Faculty for 'Health Sciences'
    for i, elem in enumerate(df['Faculty']):
        if elem == 'Health Science':
            df['Faculty'][i] = 'Health Sciences'

    # fill-in missing data for columns 4-12 (Yes, No, Not Applicable)
    for i, header in enumerate(df[:][4:13]):
        curr_col = df[header]
        for j, elem in enumerate(curr_col):
            if (pd.isnull(elem)):
                df[header][j] = 'Not Applicable' # assume Not Applicable if empty

    # fill-in missing data for columns 4-12 (Strongly Agree, Agree, ... etc.)
    for i, header in enumerate(df[:][13:]):
        curr_col = df[header]
        for j, elem in enumerate(curr_col):
            if (pd.isnull(elem)):
                df[header][j] = 'Neutral' # assume Neutral if empty

    # convert categorical strings to numerical
    for header in df[df.columns[4:]]:
        df[header] = df[header].astype('category').cat.codes

    # store dataframe to excel sheet
    writer = pd.ExcelWriter(output_file)
    df.to_excel(writer, index=False)
    writer.save()

if __name__ == "__main__":
    clean_files(mentor_input_file, mentor_output_file)
    clean_files(student_input_file, student_output_file)
