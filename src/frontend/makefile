.PHONY: match clean server docker

# -------------------------------------------------
# variable definition
# -------------------------------------------------

ORIG_MENTOR_INFILE=./data/mentors.xlsx
ORIG_STUDENT_INFILE=./data/students.xlsx

CLEAN_MENTOR_INFILE=./data/mentors-clean.xlsx
CLEAN_STUDENT_INFILE=./data/students-clean.xlsx
MATCHED_OUTFILE=./data/matched.xlsx

NEO4J_CONT_NAME=my-neo4j

all: up # default target

# -------------------------------------------------
# start and stop docker compose
# -------------------------------------------------

up:
	docker-compose up --build -d

down:
	docker-compose down

# -------------------------------------------------
# single services, typically used for testing
# -------------------------------------------------

neo4j: # run docker container for neo4j database
	docker run -d --rm --env=NEO4J_AUTH=neo4j/secret --publish=7474:7474 --publish=7687:7687 --volume=$(PWD)/src/www/dbdata:/data --name $(NEO4J_CONT_NAME) neo4j

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
