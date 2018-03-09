import argparse
import pandas as pd
import re

ans_types = {"Yes": 1, "Not Applicable": 0, "No": -1, "Strongly Agree": 2, "Slightly Agree": 1, "Agree": 1, "Neutral": 0, "Slightly Disagree": -1, "Disagree": -1, "Strongly Disagree": -2}

# starting point for the matching process
# called from the server
def clean_files(input_file, output_file):

    # load spreadsheet
    xl = pd.ExcelFile(input_file)

    # load sheet into dataframe
    df = xl.parse(xl.sheet_names[0])

    # in the headers, get rid of any extra white space
    df.columns = df.columns.str.strip()

    # in the headers, replace spaces with underscores
    df.columns = df.columns.str.replace('\s', '_')

    # clean up answers (e.g. answered more than one option)
    for i, header in enumerate (df[:][6:]): # all rows, columns 6-15

        curr_col = df[header]

        for j, cell in enumerate(curr_col):
            if re.match("(.+);(Not Applicable)", str(cell)):
                curr_col = df[header][j] = "Not Applicable"
            elif re.match("(Yes);(No)", str(cell)):
                curr_col = df[header][j] = "No"
            else:
                pass

    # replace all 'Health Science' instances under Faculty for 'Health Sciences'
    df['Faculty'].replace('Health Science', 'Health Sciences', inplace=True)

    # fill-in missing data for columns 6-15 (Yes, No, Not Applicable)
    for i, header in enumerate(df[:][6:15]):
        curr_col = df[header]
        for j, elem in enumerate(curr_col):
            if (pd.isnull(elem)):
                df.set_value(j, header, 'Not Applicable') # assume Not Applicable if empty

    # fill-in missing data for columns 15-end (Strongly Agree, Agree, ... etc.)
    for i, header in enumerate(df[:][15:]):
        curr_col = df[header]
        for j, elem in enumerate(curr_col):
            if (pd.isnull(elem) or str(elem).lower() == 'Neither Agree or Disagree'.lower()):
                df.set_value(j, header, 'Neutral')
            elif (str(elem).lower() == 'Slightly Agree'.lower()):
                df.set_value(j, header, 'Agree')
            elif (str(elem).lower() == 'Slightly Disagree'.lower()):
                df.set_value(j, header, 'Agree')

    # convert categorical strings to numerical
    for i, header in enumerate (df.iloc[:,6:]): # all rows, columns 6-15
        df[header] = df[header].map(ans_types)

    # store dataframe to excel sheet
    writer = pd.ExcelWriter(output_file)
    df.to_excel(writer, index=False)
    writer.save()

    print('> Saved to file: ' + output_file)

if __name__ == "__main__":

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

    print("\n----------------------- CLEANING DATA -----------------------")
    clean_files(mentor_input_file, mentor_output_file)
    clean_files(student_input_file, student_output_file)
    print()
