# Mentor-Student Matching

## Data Cleaning

To clean the data in question, use the python script: `root/src/clean-data.py`.

The `-h` is the help flag; when used, it will print the other available flags and options. Those in square brackets (e.g. `[-f FOO]`) are optional, while the rest are mandatory.

```
usage: clean-data.py [-h] -m MENTORINPUT -s STUDENTINPUT [-mo MENTOROUTPUT]
                     [-so STUDENTOUTPUT]

Clean mentors and students data. Note: In the clean data files, '-1' indicates
an empty field in the original excel sheet(s).

required named arguments:
  -m MENTORINPUT, --mentorinput MENTORINPUT
                        Provide the path for the INPUT file for all MENTORS
                        (.xlsx) sheet.
  -s STUDENTINPUT, --studentinput STUDENTINPUT
                        Provide the path for the INPUT file for all STUDENTS
                        (.xlsx) sheet.

optional named arguments:
  -mo MENTOROUTPUT, --mentoroutput MENTOROUTPUT
                        Provide the path for the OUTPUT file for all MENTORS
                        (.xlsx) sheet (default='mentors-clean.xlsx').
  -so STUDENTOUTPUT, --studentoutput STUDENTOUTPUT
                        Provide the path for the OUTPUT file for all STUDENTS
                        (.xlsx) sheet (default='students-clean.xlsx').
```

For example:

```
$ python clean-data.py -m ../../data/mentors.xlsx -s ../../data/students.xlsx
```

This script is meant to be used with the separate excel files under the `root/data/` directory.

## Matching Algorithm

```
1:  For each faculty:
2:      Calculate the similarity between each mentor against each student; then, create a list containing each pair and their corresponding score.
3:      Sort list of pairs and scores based on the score element, in descending order.
4:  For each tuple in the list of pairs:
5:      If the students has not been assigned or the mentor can still take more students:
            Assign the current mentee to the current mentor.
        Else:
            Skip this tuple.
```
