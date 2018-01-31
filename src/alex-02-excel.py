import pandas as pd

def load_from_excel(filename):
    xl = pd.ExcelFile(filename)
    df = xl.parse(xl.sheet_names[0])    
    return df, df.values.tolist()    

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
    
    
    # print(mentees[0])
    # print(mentees[1])



