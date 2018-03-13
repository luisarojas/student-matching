import pandas as pd
import numpy as np
from operator import itemgetter
from math import ceil, floor, exp
import json, sys
import xlsxwriter

# load data from an excel spreadsheet
def load_data(filename):
    xl = pd.ExcelFile(filename)
    df = xl.parse(xl.sheet_names[0])
    return df

def sigmoid(x):

    # if its a list: for each number in x, replace that number with its sigmoid
    if isinstance(x, (list, np.ndarray)):
        # sig_x = []
        for i, n in enumerate(x):
            x[i] = (1 / (1 + exp(-n)))
        return x
    # if its a scalar
    else:
        return 1 / (1 + exp(-x))

# calculate euclidean distance between a mentor and a mentee
def euclidean(mentor, mentee, weights):

    # if no weights are given, assign a weight of 1 to all questions
    if (len(weights) < len(mentor)):
        weights = [1] * len(mentor)

    # weights = np.reciprocal([float(w) for w in weights])

    subtr = (np.array(sigmoid(mentor))-np.array(sigmoid(mentee)))**2
    multipl = np.array([float(a)*float(b) for a, b in zip(np.array(weights), subtr)])
    d = np.sqrt(sum(multipl))
    return d

# take in mentors and mentees indices, as well as a list of their every
# combination of the two and their corresponding score
def create_groups(mentors, mentees, candidates):

    # print(candidates)

    # will hold list of all the mentees that have NOT been matched yet
    unmatched_mentees = mentees # copy

    # set the average number of mentees per mentors to be the upper bound
    MAX_NUM_MENTEES = ceil(len(mentees) / len(mentors))

    # sort the by similarity candidates so that lowest scores are at the front
    candidates_sorted = sorted(candidates, key=itemgetter(1))

    # initialize dictionary holding all the matched mentors with mentees
    # populate its keys with mentors. the values will be a list of mentees (see next step)
    matched = dict.fromkeys(mentors)

    # initialize empty list for every mentor in the dictionary
    for mentor in mentors:
        matched[mentor] = []


    # perform matching algorithm
    # set variables for mentor round-robin iteration
    target_mentor = 0
    target_lenght = len(mentors)
    while len(unmatched_mentees) > 0:
        for candidate in list(candidates_sorted):
            curr_mentor = candidate[0][0]
            curr_mentee = candidate[0][1]

            # skip current match if not the current target mentor
            if curr_mentor is not mentors[target_mentor]:
                continue

            # skip current match if mentee is already matched
            if curr_mentee not in unmatched_mentees:
                continue

            # check the number of mentees the current mentor already has assigned to them
            num_mentees_for_curr_mentor = len(matched[curr_mentor])

            # make sure that the mentor has not exceeded their limit and that the mentee has not been matched yet
            if num_mentees_for_curr_mentor < MAX_NUM_MENTEES and curr_mentee in unmatched_mentees:
                # add the current mentee to the current mentor's list in the 'matched' dictionary
                matched[curr_mentor].append(curr_mentee)
                # remove said mentee from the 'checklist' list
                unmatched_mentees.remove(curr_mentee)

                # after matching, break to look for the next target mentor
                break
        # goes to next mentor, wraps to first one if it goes out of bound
        target_mentor += 1;
        target_mentor = target_mentor % target_lenght

    # check if all mentees have been assigned
    if len(unmatched_mentees) > 0:
        if (debug):
            print("UNMATCHED:", unmatched_mentees)
        else:
            print("(" + str(len(unmatched_mentees)) + " students left umatched)... ", end='')

    return matched

# will take a key and a value (list)
def matches_to_dict(faculty, matched_indices, mentors, mentees):

    #---- Sample output ------
    # {
    #   "faculty": [
    #     {
    #       "mentor": ["name",1,2,3],
    #       "mentees": [["name",5,4,3,2],["name",54,3,1,1]]
    #     },
    #     {
    #       "mentor": ["name",1,2,3],
    #       "mentees": [["name",5,4,3,2],["name",54,3,1,1]]
    #     }
    #   ]
    # }

    # this will hold all the groups for the current faculty
    faculty_groups = {faculty: []}

    # iterate through all the mentors
    for matched_mentor_index, matched_mentee_index in matched_indices.items():
        # get the actual values of the mentor using the index
        matched_mentor = mentors[matched_mentor_index]
        # get the actual list of mentees using the indices
        matched_mentees = [mentees[i] for i in matched_mentee_index]
        # build the dict for the current mentor
        group_dict = {
            "mentor": matched_mentor,
            "mentees": matched_mentees
        }
        # add the mentor_dict to the faculty mentors
        faculty_groups[faculty].append(group_dict)

    return faculty_groups

def save_to_excel(output_filename, master_match_dict, column_names):

    for i, _ in enumerate(column_names):
        column_names[i] = column_names[i].replace('_', ' ')
        column_names[i] = column_names[i].upper()

    all_faculties_groups = []

    split_faculties_list = []

    # iterate through each faculty and their groups
    for i, faculty_dict in enumerate(master_match_dict):
        curr_faculty_groups = []

        # key -> faculty name, val -> group (mentor, [mentees])
        for key,val in faculty_dict.items():
            for group in val:
                # for each mentor, add a "MENTOR" field.
                group['mentor'] = ["MENTOR"]  + group['mentor']
                # for each mentee, add a "MENTEE" field.
                group['mentees'] = [["MENTEE"] + mentee for mentee in group['mentees']]

                curr_faculty_groups += [group['mentor']] + group['mentees']

        all_faculties_groups += curr_faculty_groups
        split_faculties_list.append(curr_faculty_groups)
        # faculty_name = list(faculty_dict.keys())[0] # current faculty name

    column_names = ["ROLE"] + column_names

    workbook = xlsxwriter.Workbook(output_filename)

    # Set formating for mentor rows
    highlight_format = workbook.add_format()
    highlight_format.set_pattern(1)
    highlight_format.set_bg_color('yellow')
    highlight_format.set_top(2)

    # Set formating for label rows
    label_format = workbook.add_format()
    label_format.set_bold()
    label_format.set_top(2)
    label_format.set_bottom(2)

    jsondata = []
    student_idx = 0

    # Create a worksheet for each faculty.
    sheet_idx = 0
    for faculty in split_faculties_list:
        # Trim faculty name for excel maximum value.
        sheet = workbook.add_worksheet(faculty[0][5][:31])
        sheet_idx += 1
        # Write the column label names
        sheet.write_row(0, 0, column_names[0:7], label_format)
        row_idx = 1
        # For every student in the faculty, write the student data.
        for row_data in faculty:
            # Mentor rows are highlighted.
            if row_data[0] == "MENTOR":
                sheet.write_row(row_idx, 0, row_data[0:7], highlight_format)
                jsondata.append({'id': student_idx, 'fname': row_data[2], 'lname': row_data[3], 'faculty': row_data[5], 'program': row_data[6], 'mentor': True})
            else:
                sheet.write_row(row_idx, 0, row_data[0:7])
                jsondata.append({'id': student_idx, 'fname': row_data[2], 'lname': row_data[3], 'faculty': row_data[5], 'program': row_data[6], 'mentor': False})
            row_idx += 1
            student_idx += 1

    # Save excel file.
    workbook.close()

    # Generate temporary json file.
    with open('./src/www/static/json/test-data.json', 'w') as outfile:
        json.dump(jsondata, outfile)

    print("\n> Saved to file: " + output_filename)

# starting point for the matching process
# called from the server
def match_all(mentors_filename, mentees_filename, output_filename, question_weights, debug):

    total_num_groups = 0

    # initialize list to hold the final matches for ALL faculties
    master_matches = []

    # load data from the mentors/mentees spreadsheets.
    # store the information in dataframe and list() formats.
    mentors_df = load_data(mentors_filename)
    mentors = mentors_df.values.tolist()
    headers = list(mentors_df.columns)

    mentees_df = load_data(mentees_filename)
    mentees = mentees_df.values.tolist()

    # create a dictionary by grouping the mentors/mentees based on faculty
    mentors_faculties = mentors_df.groupby(['Faculty']).groups
    mentees_faculties = mentees_df.groupby(['Faculty']).groups

    # compare the list of faculties of both mentor and mentee files
    # they MUST be the same faculties otherwise matching cannot work
    if list(mentors_faculties.keys()) != list(mentees_faculties.keys()):
        raise ValueError("Faculties in %s and %s do not match." % (mentors_filename, mentees_filename))
    faculties_list = list(mentors_faculties.keys())

    # print information about the mentors and mentees
    print("\n--------------------------- OVERVIEW ---------------------------")
    # mentor stats
    print("MENTORS: %d students" % len(mentors))
    for faculty, mentor_index in mentors_faculties.items():
        print(faculty + ": " + str(len(mentor_index))) # print the number of mentors in the current faculty
    print()

    # mentees stats
    print("MENTEES: %d students" % len(mentees))
    for faculty, mentee_index in mentees_faculties.items():
        print(faculty + ": " + str(len(mentee_index))) # print the number of mentors in the current faculty

    print("\n--------------------------- MATCHING ---------------------------")
    # perform matching for each of the faculties separately
    for faculty in faculties_list:

        if debug:
            print("----- %s -----" % faculty)
        else:
            print("%s... " % faculty, end='')

        faculty_mentor_indices= list(mentors_faculties[faculty]) # indices of all mentors in current faculty
        faculty_mentee_indices = list(mentees_faculties[faculty]) # indices of all mentees in current faculty

        # calculate and store the distances between every mentor and mentee in the faculty
        faculty_candidates = [] # will contain the distance between every single mentor and mentee
        # iterate through all mentors in the faculty
        for mentor_index in faculty_mentor_indices:
            curr_mentor = mentors[mentor_index][6:] # starting at column 6, since thats where the numeric columns begin
            # iterate through all mentees in the faculty
            for mentee_index in faculty_mentee_indices:
                curr_mentee = mentees[mentee_index][6:]
                # calculate the euclidean distance for each mentor vs. each mentee
                score = euclidean(curr_mentor, curr_mentee, list(question_weights.values()))
                # store the tuple and their score in the 'faculty_candidates' list
                faculty_candidates.append([(mentor_index, mentee_index), score])

        # ----------- RUN MATCHING ALGORITHM ----------
        # store the directory returned, which stores the matched indices under each mentor id
        matched_indices = create_groups(faculty_mentor_indices, faculty_mentee_indices, faculty_candidates)
        total_num_groups += len(matched_indices)

        # ----------- FACULTY RESULTS ----------
        # print the results for the current faculty
        for matched_mentor_index, matched_mentees_index in matched_indices.items():
            if debug: print(matched_mentor_index, "len: " + str(len(matched_mentees_index)), matched_mentees_index)
        print("FINISHED!")
        if debug: print()

        # convert all the indices to values (names)
        faculty_matches =  matches_to_dict(faculty, matched_indices, mentors, mentees)

        # add the current faculty to the master match list
        master_matches.append(faculty_matches)

        # move on to next faculty
        # input()

    # print("\n--------------------------- OUTPUT ---------------------------")

    # output the master match dictionary to an excel file
    save_to_excel(output_filename, master_matches, headers)

    # TEMP
    master_matches = json.dumps(temp_convert_json(master_matches))

    # return the json once the server is properly running
    # master_matches_json = json.dumps(master_matches, indent=2, sort_keys=True)

    print()

    return (master_matches, total_num_groups)

def temp_convert_json(master_matches):

    # {
    #     "faculty": [
    #         {
    #             "name": "<faculty_name>",
    #             "group": [
    #                 {
    #                     "mentor_id": "<mentor_index>",
    #                     "students":[
    #                         {
    #                             "is_mentor": "<bool>",
    #                             "id": "<mentee_id>",
    #                             "name": "<first_name>",
    #                             "surname": "<last_name>",
    #                             "email": "<e-mail>",
    #                             "program": "<program>",
    #                             "answers": [
    #                                 {
    #                                     "question_name": "<question_header>",
    #                                     "student_answer": "<mentee_answer_int>"
    #                                 },
    #                                 {
    #                                     "question_name": "<question_header>",
    #                                     "student_answer": "<mentee_answer_int>"
    #                                 }
    #                             ]
    #                         }
    #                     ]
    #                 }
    #             ]
    #         }
    #     ]
    # }

    temp_questions = ["q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10", "q11", "q12", "q13", "q14", "q15", "q16", "q17", "q18", "q19", "q20", "q21", "q22", "q23", "q24", "q25", "q26"]

    new_faculty_dict = {"Faculty":list()}
    for faculty_dict in master_matches:
        old_faculty_name = list(faculty_dict.keys())[0]
        old_faculty_groups = faculty_dict[old_faculty_name]
        #print(old_faculty_name)
        new_group_dict = {""}
        new_group_dict = {"name":old_faculty_name ,"group":list()}
        for old_group in old_faculty_groups:
            old_mentor = old_group["mentor"]
            old_mentees = old_group["mentees"]
            old_mentees.insert(0, old_mentor)
            old_students = old_mentees
            new_students_dict = {"mentor_id":old_mentor[1] ,"students": list()}
            for old_student in old_students:
                # Create the new student
                new_student = {}
                new_student["is_mentor"] = 'MENTOR' == old_student[0]
                new_student["id"] = old_student[1]
                new_student["name"] = old_student[2]
                new_student["surname"] = old_student[3]
                new_student["email"] = old_student[4]
                new_student["program"] = old_student[6]
                old_student_answers = old_student[7:]
                new_student_answers = list()
                for i,question_name in enumerate(temp_questions):
                    curr_answer = {}
                    curr_answer["question_name"] = question_name
                    curr_answer["student_answer"] = old_student_answers[i]
                    new_student_answers.append(
                        {
                            "question_name":question_name,
                            "student_answer": old_student_answers[i]
                        }
                    )
                new_student["answers"] = new_student_answers
                new_students_dict["students"].append({"student":new_student})
                #print(new_students_dict)
            new_group_dict["group"].append(new_students_dict)
        new_faculty_dict["Faculty"].append(new_group_dict)
        #print(new_group_dict)
        #input()
    return new_faculty_dict



if __name__ == "__main__": # will only be ran when script is executed from command-line

    # ------------------------ ARGS SET-UP ------------------------
    import argparse

    # set-up command-line arguments
    parser = argparse.ArgumentParser(description="Perform mentor-mentee matchmaking given an excel sheet for each.")
    parser._action_groups.pop()

    required_args = parser.add_argument_group('required named arguments')
    optional_args = parser.add_argument_group('optional named arguments')

    # add command-line argument flags and options
    required_args.add_argument('-d', action='store_true', help="Debugging flag.")
    required_args.add_argument('-m', '--mentorinput', help="Provide the path for the INPUT file for all MENTORS (.xlsx) sheet.", required=True)
    required_args.add_argument('-s', '--studentinput', help="Provide the path for the INPUT file for all STUDENTS (.xlsx) sheet.", required=True)
    optional_args.add_argument('-o', '--output', help="Provide the path for the OUTPUT file for all matches (.xlsx) (default='./data/matched.xlsx').", default="./data/matched.xlsx")

    args = parser.parse_args()

    # --------- CONFIG ---------

    # assign arguments to variables
    debug = args.d
    mentors_filename = args.mentorinput;
    mentees_filename = args.studentinput;

    output_filename = args.output # output filename - all the matched mentors/mentees will be output to this file

    #Run the matching algorithm
    master_matches_json, n = match_all(mentors_filename, mentees_filename, output_filename, dict(),debug)
