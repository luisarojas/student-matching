# ------------------------ IMPLEMENTATION ------------------------

import pandas as pd
import numpy as np
from operator import itemgetter
from math import ceil
from math import floor
import json

# load data from an excel spreadsheet
def load_data(filename):
    xl = pd.ExcelFile(filename)
    df = xl.parse(xl.sheet_names[0])
    return df

# calculate euclidean distance between a mentor and a mentee
def euclidean(mentor, mentee):
    return np.linalg.norm(np.array(mentor)-np.array(mentee))

# take in mentors and mentees indices, as well as a list of their every
# combination of the two and their corresponding score
def match(mentors, mentees, candidates):

    # will hold list of all the mentees that have NOT been matched yet
    unmatched_mentees = mentees # copy

    # set the average number of mentees per mentors to be the upper bound
    MAX_NUM_MENTEES = ceil(len(mentees) / len(mentors))

    # sort the by similarity candidates so that lowest scores are at the front
    candidates_sorted = sorted(candidates, key=itemgetter(1))

    # dictionary holding all the matched mentors with mentees
    # populate its keys with mentors. the values will be a list of mentees (see next step)
    matched = dict.fromkeys(mentors)

    # initialize empty list for every mentor in the dictionary
    for mentor in mentors:
        matched[mentor] = []

    # perform matching algorithm
    for candidate in candidates_sorted:

        curr_mentor = candidate[0][0]
        curr_mentee = candidate[0][1]

        # check the number of mentees the current mentor already has assigned to them
        num_mentees_for_curr_mentor = len(matched[curr_mentor])

        # make sure that the mentor has not exceeded their limit and that the mentee has not been matched yet
        if num_mentees_for_curr_mentor < MAX_NUM_MENTEES and curr_mentee in unmatched_mentees:
            # add the current mentee to the current mentor's list in the 'matched' dictionary
            matched[curr_mentor].append(curr_mentee)
            # remove said mentee from the 'checklist' list
            unmatched_mentees.remove(curr_mentee)

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
        # faculty_name = list(faculty_dict.keys())[0] # current faculty name

    column_names = ["ROLE"] + column_names

    # generate dataframe
    df = (pd.DataFrame(all_faculties_groups, columns=column_names))
    split_df = df.groupby(['FACULTY'])

    writer = pd.ExcelWriter(output_filename)
    for group_tuple in split_df:
        sheet_name = group_tuple[0][:31] # truncate faculty name to 31 characters max
        group_tuple[1].iloc[:, :7].to_excel(writer, sheet_name,index=False) # select only the first 7 columns
    writer.save()

    print("\n> Saved to file: " + output_filename)

def run_match_alg(mentors_filename, mentees_filename, output_filename, debug):
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
                score = euclidean(curr_mentor, curr_mentee)
                # store the tuple and their score in the 'faculty_candidates' list
                faculty_candidates.append([(mentor_index, mentee_index), score])

        # ----------- RUN MATCHING ALGORITHM ----------
        # store the directory returned, which stores the matched indices under each mentor id
        matched_indices = match(faculty_mentor_indices, faculty_mentee_indices, faculty_candidates)

        # ----------- FACULTY RESULTS ----------
        # print the results for the current faculty
        for matched_mentor_index, matched_mentees_index in matched_indices.items():
            if debug: print(matched_mentor_index, matched_mentees_index)
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

    # return the json once the server is properly running
    master_matches_json = json.dumps(master_matches)

    print()

    return master_matches_json


if __name__ == "__main__":
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
    master_matches_json = run_match_alg(mentors_filename, mentees_filename, output_filename, debug)
