import os
from flask import Flask
from flask import render_template, request, json, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import sys

#Matching related variables
sys.path.append("./src/")
from match import match

#Data cleaning
sys.path.append("./src/data-cleaning")
from clean_data import clean_files

#Global Variables
UPLOAD_FOLDER="./src/www/uploads/"
DOWNLOAD_FOLDER="./src/www/downloads/"
MATCH_OUTPUT_FILE = "matched.xlsx"
ALLOWED_EXTENSIONS = set(['txt', 'xlsx'])

#Define the app
app = Flask(__name__)

#APP configurations
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# define basic route
@app.route("/")
def printData():
    return render_template('data.html', title="Mentor Mentee Matching")

@app.route('/uploader', methods = ['POST'])
def uploader():
    req_mentor_file = "mentor_file" # html form field "name"
    req_mentee_file = "student_file" # html form field "name"

    print("uploader() called")
    print("files:", request.files[req_mentor_file], request.files[req_mentee_file])

    #Ensure that the request has the file part
    if req_mentor_file not in request.files or req_mentee_file not in request.files:
        error = "ERROR: post request missing file part"
        return error

    obj_mentor_file = request.files[req_mentor_file]
    obj_mentee_file = request.files[req_mentee_file]

    #Check if request was submitted without a file
    if obj_mentor_file.filename == "" or obj_mentee_file.filename == "":
        error = "ERROR: User did not attach a file"
        return error

    #Actually submitted a file
    if obj_mentor_file and allowed_file(obj_mentor_file.filename) and\
       obj_mentee_file and allowed_file(obj_mentee_file.filename):
        mentor_filename  = secure_filename(obj_mentor_file.filename)
        mentee_filename  = secure_filename(obj_mentee_file.filename)

        obj_mentor_file.save(os.path.join(app.config['UPLOAD_FOLDER'], mentor_filename))
        obj_mentee_file.save(os.path.join(app.config['UPLOAD_FOLDER'], mentee_filename))
        print("UPLOAD SUCCESS")

        print('> Cleaning data...')
        #Clean the data- save in the downloads folder
        clean_files(app.config['UPLOAD_FOLDER'] + mentor_filename, app.config['DOWNLOAD_FOLDER'] + "clean_" + mentor_filename)
        clean_files(app.config['UPLOAD_FOLDER'] + mentee_filename, app.config['DOWNLOAD_FOLDER'] + "clean_" + mentee_filename)

        print('> Running matching algorithm...')
        #Run the algorithm
        json_data = match(app.config['DOWNLOAD_FOLDER'] + "clean_" + mentor_filename,\
                          app.config['DOWNLOAD_FOLDER'] + "clean_" + mentee_filename, \
                          app.config['DOWNLOAD_FOLDER'] + MATCH_OUTPUT_FILE, True)
        return json_data

    return "UPLOAD UNSUCCESSFUL"

# check if the executed file is the main program
if __name__ == "__main__":
    app.run(port=5000) # run the app
