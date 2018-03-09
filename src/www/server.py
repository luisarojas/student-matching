from flask import Flask, render_template, request, send_file
from werkzeug import secure_filename
from pandas import ExcelFile
import json, os, sys, math
import pandas as pd
import numpy as np

app = Flask(__name__)

# matching and data cleaning-related variables
sys.path.append("./src/scripts/")
from match import match_all
from clean_data import clean_files

#Neo4j
from neo4j.v1 import GraphDatabase, basic_auth

# global variables
MENTOR_FILENAME = ""
STUDENT_FILENAME = ""
SUCCESS_CODE = 1
FAILURE_CODE = -1
ALLOWED_FILE_EXTENSIONS = set(['xlsx'])
UPLOAD_FOLDER="./src/www/uploads/"
DOWNLOAD_FOLDER="./src/www/downloads/"
MATCH_OUTPUT_FILE = "matched.xlsx"

# app configurations
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

def is_extension_allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_FILE_EXTENSIONS

def validate_upload_files(mentorfile, studentfile):

    required_fields = ["Student ID", "First Name", "Last Name", "E-mail", "Faculty", "Program"]
    accepted_ans_types = ["No", "Yes", "Not Applicable", "Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"]

    mentorsdf = pd.read_excel(mentorfile)
    studentsdf = pd.read_excel(studentfile)

    all_mentor_answers = pd.unique(mentorsdf.iloc[:,6:].values.ravel('K'))
    all_mentor_answers = [x for x in all_mentor_answers if not pd.isnull(x)]

    all_student_answers = pd.unique(studentsdf.iloc[:,6:].values.ravel('K'))
    all_student_answers = [x for x in all_student_answers if not pd.isnull(x)]

    mentors_file_headers = mentorsdf.columns.tolist()
    students_file_headers = studentsdf.columns.tolist()

    # ignore null values - they would be filled in when cleaning the data
    if (set(all_mentor_answers) != set(accepted_ans_types)):
        return {"message": "Your mentor file contains answer types that are not supported.", "code": FAILURE_CODE}

    if (set(all_student_answers) != set(accepted_ans_types)):
        return {"message": "Your student file contains answer types that are not supported.", "code": FAILURE_CODE}

    if (set(mentorsdf['Faculty'].unique()) != set(studentsdf['Faculty'].unique())):
        return {"message": "The Faculties listed are not the same in both files.", "code": FAILURE_CODE}

    if ([h.strip().lower() for h in mentors_file_headers] != [h.strip().lower() for h in students_file_headers]):
        return {"message": "The columns in the files submitted do not match.", "code": FAILURE_CODE}

    first_n_columns = mentors_file_headers[:len(required_fields)]
    if ([h.strip().lower() for h in first_n_columns] != [h.strip().lower() for h in required_fields]):
        return {"message": "The first " + str(len(required_fields)) + " columns of some file(s) do not match the required format.", "code": FAILURE_CODE}

    if (len(mentorsdf.index) >= len(studentsdf.index)):
        return {"message": "Please make sure you have uploaded the files in the right order.", "code": FAILURE_CODE}

    return {"message": "The files were successfully validated.", "code": SUCCESS_CODE, "num_students": len(mentorsdf.index)+len(studentsdf.index)}

# define basic route
@app.route("/")
def main():
    return render_template('index.html')

@app.route("/home", methods=['POST'])
def home():
    return render_template('home.html')

@app.route("/newMatchStep1", methods=['POST'])
def new_match_s1():
    return render_template('newmatch-step1.html')

@app.route('/newMatchStep2', methods = ['POST', 'GET'])
def new_match_s2():

    default_value = 3

    htmltable = "<table id=\"questions-table\" class=\"table table-bordered table-sm\"><thead class=\"thead-light\"><tr><th>QUESTION</th><th>WEIGHT</th></tr></thead><tbody>"
    question_headers = pd.read_excel(app.config['UPLOAD_FOLDER'] + MENTOR_FILENAME).columns.tolist()

    for header in question_headers[6:]:
        htmltable += "<tr><td>" + header + "</td><td><input style=\"width:100%\" type=\"number\" min=\"0\" max=\"5\" step=\"1\" value=\"" + str(default_value) + "\"></td></tr>"
    htmltable += "</tbody></table>"

    return json.dumps({"message": "Grabbed the header information successfully.", "code": SUCCESS_CODE, "html": render_template('newmatch-step2.html'), "htmltable": htmltable})

@app.route("/lastMatch", methods=['POST']) # default is GET
def last_match():
    return render_template('lastmatch.html')

@app.route("/mentorLogs", methods=['POST']) # default is GET
def mentor_logs():
    return render_template('mentorLogs.html')

@app.route("/feedback", methods=['POST']) # default is GET
def feedback():
    return render_template('feedback.html')

@app.route('/upload', methods = ['POST'])
def uploader():

    # TODO: grab this from the request
    mentor_input_name = "mentor_file" # html form field "name"
    student_input_name = "student_file" # html form field "name"

    mentor_file = request.files[mentor_input_name]
    student_file = request.files[student_input_name]

    # error if the request was submitted without a file
    if not mentor_file or not student_file or mentor_file == "" or student_file == "":
        FAILURE_DATA = {"message": "Please attach mentor and student files.", "code": FAILURE_CODE}
        return json.dumps(FAILURE_DATA)

    # if the extensions submitted are not allowed
    if not is_extension_allowed(mentor_file.filename) or not is_extension_allowed(student_file.filename):
        FAILURE_DATA = {"message": "Please only submit Excel (.xlsx) files.", "code": FAILURE_CODE}
        return json.dumps(FAILURE_DATA)

    # secure filename
    global MENTOR_FILENAME, STUDENT_FILENAME
    MENTOR_FILENAME = secure_filename(mentor_file.filename)
    STUDENT_FILENAME = secure_filename(student_file.filename)

    # save files to server
    mentor_file.save(os.path.join(app.config['UPLOAD_FOLDER'], MENTOR_FILENAME))
    student_file.save(os.path.join(app.config['UPLOAD_FOLDER'], STUDENT_FILENAME))

    # make sure both files follow the same structure, in terms of columns
    # make sure the mentor and student files were not uploaded in reverse
    result = validate_upload_files(app.config['UPLOAD_FOLDER'] + MENTOR_FILENAME, app.config['UPLOAD_FOLDER'] + STUDENT_FILENAME)
    if result['code'] == FAILURE_CODE:
        FAILURE_DATA = {"message": result['message'], "code": FAILURE_CODE}
        return json.dumps(FAILURE_DATA)

    # success!
    SUCCESS_DATA = {"message": "The files were uploaded successfully.", "code": SUCCESS_CODE, "numStudents": result['num_students']}
    return json.dumps(SUCCESS_DATA)

@app.route('/match', methods = ['POST'])
def match():

    # receive array of json objects
    req_data_questions = request.get_json()['questions']

    # convert to dictionary
    questions_weights = dict()
    for row in req_data_questions:
        questions_weights[row['header']] = row['weight']

    # clean data
    print("\nCleaning data...")
    clean_files(app.config['UPLOAD_FOLDER'] + MENTOR_FILENAME, app.config['UPLOAD_FOLDER'] + "clean_" + MENTOR_FILENAME)
    clean_files(app.config['UPLOAD_FOLDER'] + STUDENT_FILENAME, app.config['UPLOAD_FOLDER'] + "clean_" + STUDENT_FILENAME)

    # run matching algorithm
    print("\nMatching...")
    match_data, total_num_groups = match_all(app.config['UPLOAD_FOLDER'] + "clean_" + MENTOR_FILENAME,\
                                    app.config['UPLOAD_FOLDER'] + "clean_" + STUDENT_FILENAME, \
                                    app.config['DOWNLOAD_FOLDER'] + MATCH_OUTPUT_FILE, questions_weights, False)

    # TODO: store in database

    SUCCESS_DATA = {"message": "Successfully created " + str(total_num_groups) + " groups.", "code": SUCCESS_CODE, "numGroups": total_num_groups}
    return json.dumps(SUCCESS_DATA)

@app.route('/download', methods = ['GET'])
def download_match():
    return send_file("downloads/" + MATCH_OUTPUT_FILE, as_attachment=True)

@app.route('/test_neo4j')
def test_neo4j():
    print("/test_neo4j called")
    driver = GraphDatabase.driver("bolt://neo4j:7687", auth=basic_auth("neo4j","secret"))
    return "OK"

@app.route('/test_match')
def test_json():
    print("/test_match called")

    return "OK"

# check if the executed file is the main program
if __name__ == "__main__":
    # app.run(port=5000) # run the app
    app.run(host="0.0.0.0", debug=True)
