# Mentor-Student Matching

## Data Cleaning

To clean the data in question, use the python script: `src/clean-data.py`. It can be used the following way:

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

This script is meant to be used with the previously-generated data, created from the original _(provided)_.
