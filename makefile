.PHONY: match clean server

ORIG_MENTOR_INFILE=./data/mentors.xlsx
ORIG_STUDENT_INFILE=./data/students.xlsx

CLEAN_MENTOR_INFILE=./data/mentors-clean.xlsx
CLEAN_STUDENT_INFILE=./data/students-clean.xlsx
MATCHED_OUTFILE=./data/matched.xlsx

NEO4J_CONT_NAME=my-neo4j

all: neo4j serve

neo4j:
	docker run -d --rm --env=NEO4J_AUTH=neo4j/foobar --publish=7474:7474 --publish=7687:7687 --volume=$(PWD)/src/www/dbdata:/data --name $(NEO4J_CONT_NAME) neo4j

serve:
	python ./src/www/server.py

stop-neo4j:
	docker stop $(NEO4J_CONT_NAME)
	docker ps -a

match: clean
	python ./src/scripts/match.py -m $(CLEAN_MENTOR_INFILE) -s $(CLEAN_STUDENT_INFILE) -o $(MATCHED_OUTFILE)

clean:
	python ./src/scripts/clean_data.py -m $(ORIG_MENTOR_INFILE) -s $(ORIG_STUDENT_INFILE) -mo $(CLEAN_MENTOR_INFILE) -so $(CLEAN_STUDENT_INFILE)

clear:
	rm $(CLEAN_MENTOR_INFILE) $(CLEAN_STUDENT_INFILE) $(MATCHED_OUTFILE)
