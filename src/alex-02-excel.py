import pandas as pd
import numpy as np
from operator import itemgetter
from math import ceil

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


if __name__ == "__main__":
    #---------CONFIG---------
    mentors_filename = "../data/mentors-clean.xlsx"
    mentees_filename = "../data/students-clean.xlsx"
    
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
        print("-----%s-----" % faculty)
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
        #matched = match_alg1()
        matched = match_alg2(mentors_num, mentees_num)


        for matched_mentor_i, matched_mentees_i in matched.items():
            print(matched_mentor_i, matched_mentees_i)
        print("DONE!\n")
        #input()
        
    

    
    # print(mentees[0])
    # print(mentees[1])



