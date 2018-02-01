debug = True
# ------------------------ ARGS SET-UP ------------------------
import argparse
import numpy as np
import random

# set-up command-line arguments
parser = argparse.ArgumentParser(description="Run k-means clustering on mentors and first-year students.")
parser._action_groups.pop()

required_args = parser.add_argument_group('required named arguments')

# add command-line argument flags and options
required_args.add_argument('-m', '--mentorinput', help="Provide the path for the INPUT file for all MENTORS (.xlsx) sheet.", required=True)
required_args.add_argument('-s', '--studentinput', help="Provide the path for the INPUT file for all STUDENTS (.xlsx) sheet.", required=True)
args = parser.parse_args()

# assign arguments to variables
mentor_input_file = args.mentorinput;
student_input_file = args.studentinput;

# ------------------------ FUNCTION DEFINITIONS ------------------------

import pandas as pd
from sklearn.cluster import KMeans

# sum of squares error
def distance(d):
    u = centroid(d)
    return np.sum(np.linalg.norm(np.asarray(d, dtype='float') - np.asarray(u, dtype='float'), 2, 1))

# find centroid of given data
def centroid(d):
    return np.mean(d, 0, dtype=np.float64)

# ------------------------ K-MEANS ------------------------

def kmeans(df, K):

    MIN_GAIN = 0.01 # minimum gain to keep on iterating
    MAX_ITERS = 100 # maximum number of iterations to perform
    MAX_EPOCHS = 10 # number of random starts to find global optimum
    if (debug):
        MAX_EPOCHS = 1

    # data = np.matrix(df)[:, 6:]
    data = np.matrix(df)
    # print(data)

    error = np.inf # starting error
    # multiple (random) initializations for global optimum
    for epoch in range(MAX_EPOCHS):

        # initialize K centroids
        indices = np.random.choice(len(data), K, replace=False)
        # print (indices)

        # select only the rows in 'indices', and columns 6 to the end
        u = (data[indices, :])
        # print(u[:, 6:])

        # loop through all elements in the pool
        curr_iter = 0
        old_sse = np.inf

        # while True:
        while curr_iter < 10:

            curr_iter += 1
            # print(curr_iter)

            # assign to a cluster
            clusters = [None] * K # initialize empty clusters list

            for row in data:
                # print(row[:, 6:])
                j = np.argmin(np.linalg.norm(np.asarray(row[:, 6:], dtype='float')-np.asarray(u[:, 6:], dtype='float'), 2, 1))

                if (clusters[j] is None):
                    clusters[j] = row
                else:
                    np.vstack((clusters[j], row))

            # centroid update
            for j in range(K):
                u[j] = centroid(clusters[j])

    return "", ""

# ------------------------ MAIN FUNCTIONALITY ------------------------
if __name__ == "__main__":

    # print("Loading data...")

    # load spreadsheets
    xl_mentors = pd.ExcelFile(mentor_input_file)
    xl_students = pd.ExcelFile(student_input_file)

    # load the first sheet into a DataFrame by name: df
    df_mentors = xl_mentors.parse(xl_mentors.sheet_names[0])
    df_students = xl_students.parse(xl_students.sheet_names[0])

    # print("Clustering...")

    # insert new column 'is_mentor'
    df_mentors.insert(0, 'is_mentor', 'True')
    df_students.insert(0, 'is_mentor', 'False')

    # merge both dataframes vertically
    NUM_MENTORS = df_mentors.shape[0]
    df = pd.concat([df_mentors, df_students])
    # df = df.reset_index()
    df.insert(0, 'index', range(len(df)))

    clusters, mu = kmeans(df, NUM_MENTORS) # data, k
    # for i, row in enumerate(clusters):
    #     print(str(i) + " " + str(row))
