.PHONY: match clean server

ORIG_MENTOR_INFILE=./data/mentors.xlsx
ORIG_STUDENT_INFILE=./data/students.xlsx

CLEAN_MENTOR_INFILE=./data/mentors-clean.xlsx
CLEAN_STUDENT_INFILE=./data/students-clean.xlsx
MATCHED_OUTFILE=./data/matched.xlsx

match: clean
	python ./src/match.py -m $(CLEAN_MENTOR_INFILE) -s $(CLEAN_STUDENT_INFILE) -o $(MATCHED_OUTFILE)

clean:
	python ./src/data-cleaning/clean-data.py -m $(ORIG_MENTOR_INFILE) -s $(ORIG_STUDENT_INFILE) -mo $(CLEAN_MENTOR_INFILE) -so $(CLEAN_STUDENT_INFILE)

server:
	python ./src/www/server.py

clear:
	rm $(CLEAN_MENTOR_INFILE) $(CLEAN_STUDENT_INFILE) $(MATCHED_OUTFILE)
