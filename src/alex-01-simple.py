import numpy as np
from operator import itemgetter

debug=True

def euclidean(mentor, mentee):
    return np.linalg.norm(mentor-mentee)    

if __name__ == "__main__":
    #---------CONFIG---------
    MAX_NUM_MENTEES = 4
    
    #---------MENTEES---------
    p1 = np.array([1,2,3,4])
    p2 = np.array([4,3,2,1])
    p3 = np.array([2,4,1,3])
    p4 = np.array([3,4,1,2])
    p5 = np.array([1,4,2,3])
    p6 = np.array([1,3,2,4])
    p7 = np.array([1,3,2,4])
    mentees = [p1,p2,p3,p4,p5,p6,p7]
    mentee_checklist = [False]*len(mentees) #Keeps tracks of which mentees have been accounted for
    
    #---------MENTORS---------
    M1 = np.array([1,2,3,4])
    M2 = np.array([4,3,2,1])
    mentors = [M1, M2]
    mentor_indeces = list(range(0,len(mentors)))  

    raw_matches = list()
    for i_mentor, mentor in enumerate(mentors):
        for i_mentee, mentee in enumerate(mentees):
            dist = euclidean(mentor, mentee)
            if debug: print("([%d]" % i_mentor, mentor,")", "---->matching----->","([%d]" %i_mentee,mentee,")","= %f" % dist )
            match = [i_mentor, i_mentee, dist]
            raw_matches.append(match)
        print("------------------")

    print("------------------RAW SORTED SCORES------------------")
    #Sort the raw_matches by lowest distance
    raw_matches = sorted(raw_matches, key=itemgetter(2))

    #Dictionary with the mentor indices as the keys and the values as the list of mentee indices
    matches = dict.fromkeys(mentor_indeces)
    #Init the matches with only lists
    for i in range(len(mentors)):
        matches[i] = list()
    
    for match in raw_matches:
        curr_mentor_index = match[0]
        curr_mentee_index = match[1]
        curr_mentee_count = len(matches[curr_mentor_index])
        if not mentee_checklist[curr_mentee_index] and curr_mentee_count < MAX_NUM_MENTEES:
            matches[curr_mentor_index].append(curr_mentee_index)
            mentee_checklist[curr_mentee_index] = True
        if debug: print(match)

    print("------------------UNMATCHED STUDENTS------------------")
    #Get the indices of all the mentees that haven't been matched yet
    unmatched_mentee_indices = [i for i, mentee_matched in enumerate(mentee_checklist) if not mentee_matched]
    if debug: print(mentee_checklist)
    print(unmatched_mentee_indices)

    #Add those unmatched mentees to the best mentor regardless of the limit
    # for match in raw_matches:
    #     curr_mentor_index = match[0]
    #     curr_mentee_index = match[1]
    #     if not mentee_checklist[curr_mentee_index]:
    #         matches[curr_mentor_index].append(curr_mentee_index)
    #         mentee_checklist[curr_mentee_index] = True
    

    print("------------------FINAL_RESULTS------------------")
    print(matches)

    
    



        
    
    
