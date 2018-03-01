from flask import Flask, render_template, request
import json

app = Flask(__name__)

pythonDictionary = {'name':'Bob', 'age':44, 'isEmployed':True}
dictionaryToJson = json.dumps(pythonDictionary)

SUCCESS_CODE = {"message": "The process was carried out successfully.", "code": 100}
FAILURE_CODE = {"message": "The process could not be completed.", "code": 200}

# define basic route
@app.route("/")
def main():
    return render_template('index.html')

@app.route("/home", methods=['POST'])
def home():
    return render_template('home.html')

@app.route("/newMatch", methods=['POST'])
def new_match():
    return render_template('newmatch.html')

@app.route('/upload', methods = ['POST'])
def uploader():

    # TODO: grab this from the request
    mentor_input_name = "mentor_file" # html form field "name"
    student_input_name = "student_file" # html form field "name"

    mentor_file = request.files[student_input_name]
    student_file = request.files[student_input_name]

    print("files:", mentor_file, student_file)
    return json.dumps(SUCCESS_CODE)

@app.route("/lastMatch", methods=['POST']) # default is GET
def last_match():
    return render_template('lastmatch.html')

@app.route("/mentorLogs", methods=['POST']) # default is GET
def mentor_logs():
    return render_template('mentorLogs.html')

@app.route("/feedback", methods=['POST']) # default is GET
def feedback():
    return render_template('feedback.html')

# check if the executed file is the main program
if __name__ == "__main__":
    app.run(port=5000) # run the app
