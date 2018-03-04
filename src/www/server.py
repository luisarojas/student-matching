from flask import Flask, render_template, request
from werkzeug import secure_filename
from pandas import ExcelFile
import json, os, sys
import pandas as pd

app = Flask(__name__)

# TODO: This will be uncommented when we start developing "Step 2"
# matching and data cleaning-related variables
# sys.path.append("./src/scripts")
# from match import match
# from clean_data import clean_files

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

    mentorsdf = pd.read_excel(mentorfile)
    studentsdf = pd.read_excel(studentfile)

    print(len(mentorsdf.index), len(studentsdf.index))

    if (mentorsdf.columns.tolist() != studentsdf.columns.tolist()):
        return {"message": "The columns in the files submitted do not match.", "code": FAILURE_CODE}

    if (len(mentorsdf.index) >= len(studentsdf.index)):
        return {"message": "Please make sure you have uploaded the files in the right order.", "code": FAILURE_CODE}

    return {"message": "The files were successfully validated.", "code": SUCCESS_CODE}

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

    for header in question_headers:
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
    SUCCESS_DATA = {"message": "The files were uploaded successfully.", "code": SUCCESS_CODE}
    return json.dumps(SUCCESS_DATA)

# check if the executed file is the main program
if __name__ == "__main__":
    app.run(port=5000) # run the app
