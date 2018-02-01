import pandas as pd
import numpy as np
from operator import itemgetter
from math import ceil
from math import floor
import json

def load_from_excel(filename):
    xl = pd.ExcelFile(filename)
    df = xl.parse(xl.sheet_names[0])
    return df, df.values.tolist()

def euclidean(mentor, mentee):
    return np.linalg.norm(np.array(mentor)-np.array(mentee))

def match_alg1():
    #Sort the candidates so that lowest scores are at the front
    candidates_sorted = sorted(candidates, key=itemgetter(1))

    #This will be the dictionary holding all the matched mentors with mentees
    matched = dict.fromkeys(mentors_i)
    #Initialize the empty list for every mentor in the dictionary
    for i in mentors_i:
        matched[i] = list()

    #Perform the actual algorithm to match
    for candidate in candidates_sorted:
        mentor_i = candidate[0][0]
        mentee_i = candidate[0][1]
        score = candidate[1]
        #Make sure that the mentee has not been matched yet
        if mentee_i in mentee_checklist:
            matched[mentor_i].append(mentee_i)
            mentee_checklist.remove(mentee_i)

    return matched

def match_alg2(mentors_num, mentees_num):
    avg_num_mentees = ceil(mentees_num / mentors_num)
    # print("mentors_num=", mentors_num)
    # print("mentees_num=", mentees_num)
    # print("avg_num_mentees=", avg_num_mentees)

    #Sort the candidates so that lowest scores are at the front
    candidates_sorted = sorted(candidates, key=itemgetter(1))

    #This will be the dictionary holding all the matched mentors with mentees
    matched = dict.fromkeys(mentors_i)
    #Initialize the empty list for every mentor in the dictionary
    for i in mentors_i:
        matched[i] = list()

    #Perform the actual algorithm to match
    for candidate in candidates_sorted:
        mentor_i = candidate[0][0]
        mentee_i = candidate[0][1]
        score = candidate[1]
        num_mentees_for_curr_mentor = len(matched[mentor_i])
        #Make sure that the mentee has not been matched yet
        if num_mentees_for_curr_mentor < avg_num_mentees and mentee_i in mentee_checklist:
            matched[mentor_i].append(mentee_i)
            mentee_checklist.remove(mentee_i)

    #-------------UNMATCHED-------------
    #Check to see if there are any unmatched students
    if len(mentee_checklist) > 0:
        print("UNMATCHED:", mentee_checklist)

    return matched


def build_faculty_dict(matched_i):
    #----Same output------
    # {
    #   "mentors": [
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

    #This will hold all the mentors for the current faculty
    faculty_dict = {"mentors": list()}
    #Iterate through all the mentors
    for matched_mentor_i, matched_mentees_i in matched_i.items():
        #Get the actual values of the mentor using the index
        matched_mentor = mentors[matched_mentor_i]
        #Get the actual list of mentees using the indices
        matched_mentees = [mentees[matched_mentee_i] for matched_mentee_i in matched_mentees_i]
        #Build the dict for the current mentor
        mentor_dict = {
            "mentor": matched_mentor,
            "mentees": matched_mentees
        }
        #Add the mentor_dict to the faculty mentors
        faculty_dict["mentors"].append(mentor_dict)

    return faculty_dict

def save_to_excel(output_filename, master_match_dict):
    all_groups = list()
    for faculty, mentors_dict in master_match_dict.items():
        mentors = mentors_dict["mentors"]
        for mentor_info in mentors:
            mentor = mentor_info["mentor"]
            mentor_prepended = ["MENTOR"] + mentor
            mentees = mentor_info["mentees"]
            mentees_prepended = [["MENTEE"] + mentee for mentee in mentees]

            #Create the group
            group = [mentor_prepended] + mentees_prepended
            all_groups = all_groups + group

    #Create the dataframe
    df = pd.DataFrame(all_groups)
    writer = pd.ExcelWriter(output_filename)
    df.to_excel(writer, index=False)
    writer.save()
    print("Saved to file:", output_filename)


if __name__ == "__main__":
    #---------CONFIG---------
    #If intermediate information is printed (during dev cycle)
    debug = False

    #This dictionary will hold the final matches for each faculty
    master_match_dict = {}

    #Input filenames
    mentors_filename = "../data/mentors-clean.xlsx"
    mentees_filename = "../data/students-clean.xlsx"

    #Output filename - all the matched mentors/mentees will be output to this file
    output_filename = "../data/AUTO-MATCHED.xlsx"

    #Load the mentors/mentees spreadsheet
    mentors_df, mentors = load_from_excel(mentors_filename)
    mentees_df, mentees = load_from_excel(mentees_filename)

    #Group the mentors/mentees based on faculty
    mentors_faculties = mentors_df.groupby(['Faculty']).groups
    mentees_faculties = mentees_df.groupby(['Faculty']).groups

    #Compare the list of faculties of both mentor and mentee files
    # they MUST be the same faculties otherwise matching cannot work
    if list(mentors_faculties.keys()) != list(mentees_faculties.keys()):
        raise ValueError("Faculties Column in %s and %s do not match!" % (mentors_filename, mentees_filename))
    faculties_list = list(mentors_faculties.keys())

    #Print Information about the mentors and mentees
    print("---------------------------STATS---------------------------")
    #Mentors
    print("MENTORS: %d students" % len(mentors))
    print("Faculties:")
    for faculty, mentor_indices in mentors_faculties.items():
        print(faculty, ":", len(mentor_indices))
    print("---------")
    #Mentors
    print("MENTEES: %d students" % len(mentees))
    print("Faculties:")
    for faculty, mentee_indices in mentees_faculties.items():
        print(faculty, ":", len(mentee_indices))


    print("---------------------------MATCHING---------------------------")
    #Perform matching for each of the faculties separately
    for faculty in faculties_list:
        if debug:
            print("-----%s-----" % faculty)
        else:
            print("%s... " % faculty, end='')
        mentors_i = list(mentors_faculties[faculty]) #Indices of all mentors in current faculty
        mentees_i = list(mentees_faculties[faculty]) #Indices of all mentees in current faculty

        #Get the number of mentors and mentees for the faculty
        mentors_num = len(mentors_i)
        mentees_num = len(mentees_i)

        #Will hold list of all the mentees hat have NOT been matched yet
        #mentee_checklist = dict.fromkeys(mentees_i, False)
        mentee_checklist = mentees_i.copy()

        #This will contain the distance between every single mentor and mentee
        candidates = list()

        #Cacluate the distances between every mentor and mentee in the faculty
        for mentor_i in mentors_i:
            curr_mentor = mentors[mentor_i][4:] #4 since the numeric columns start on the 5th col
            for mentee_i in mentees_i:
                curr_mentee = mentees[mentee_i][4:]
                score = euclidean(curr_mentor, curr_mentee)
                candidates.append([(mentor_i, mentee_i), score])

        # -----------START MATCHING----------
        #matched_i = match_alg1()
        matched_i = match_alg2(mentors_num, mentees_num)

        # -----------FACULTY RESULTS----------
        #Print the results for the faculty
        for matched_mentor_i, matched_mentees_i in matched_i.items():
            if debug: print(matched_mentor_i, matched_mentees_i)
        print("DONE!")
        if debug: print()

        #Convert all the indices to actual values(names)
        faculty_dict = build_faculty_dict(matched_i)

        #Add the current faculty to the final master match list
        master_match_dict[faculty] = faculty_dict

    print("---------------------------OUTPUT---------------------------")

    #Return the json once the server is properly running
    master_match_json = json.dumps(master_match_dict)

    #Output the master match dictionary to an excel file
    save_to_excel(output_filename, master_match_dict)
