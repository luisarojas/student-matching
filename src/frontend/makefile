.PHONY: match clean serve

# -------------------------------------------------
# variable definition
# -------------------------------------------------

ORIG_MENTOR_INFILE=./data/mentors.xlsx
ORIG_STUDENT_INFILE=./data/students.xlsx

CLEAN_MENTOR_INFILE=./data/mentors-clean.xlsx
CLEAN_STUDENT_INFILE=./data/students-clean.xlsx
MATCHED_OUTFILE=./data/matched.xlsx

all: serve # default target

# -------------------------------------------------
# single services, typically used for testing
# -------------------------------------------------

serve:
	python ./src/www/server.py

match: clean # run matching algorithm
	python ./src/scripts/match.py -m $(CLEAN_MENTOR_INFILE) -s $(CLEAN_STUDENT_INFILE) -o $(MATCHED_OUTFILE)

clean: # clean data
	python ./src/scripts/clean_data.py -m $(ORIG_MENTOR_INFILE) -s $(ORIG_STUDENT_INFILE) -mo $(CLEAN_MENTOR_INFILE) -so $(CLEAN_STUDENT_INFILE)

# -------------------------------------------------
# clear directories
# -------------------------------------------------

clear:
	rm $(CLEAN_MENTOR_INFILE) $(CLEAN_STUDENT_INFILE) $(MATCHED_OUTFILE)
