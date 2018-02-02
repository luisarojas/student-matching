import os
from flask import Flask
from flask import render_template, request, json, redirect, url_for, send_from_directory
from werkzeug import secure_filename

#Global Variables
UPLOAD_FOLDER="./src/www/uploads/"
ALLOWED_EXTENSIONS = set(['txt', 'xlsx'])

#Define the app
app = Flask(__name__)

#APP configurations
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# define basic route
@app.route("/")
def printData():
    return render_template('data.html', title="Mentor Mentee Matching")

	
@app.route('/uploader', methods = ['POST'])
def uploader():
    print("uploader() called")
    print("files:", request.files["file"])
    if request.method == "POST":
        #Ensure that the request has the file part
        if "file" not in request.files:
            error = "ERROR:", "post request missing file part"
            return error

        client_file = request.files["file"]
        #Check if request was submitted without a file
        if client_file.filename == "":
            error = "ERROR:", "User did not attach a file"
            return error

        #Actually submitted a file
        if client_file and allowed_file(client_file.filename):
            filename  = secure_filename(client_file.filename)
            client_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "UPLOAD SUCCESS"


    return "UPLOAD UNSUCCESSFUL"

@app.route("/test", methods=['GET'])
def test():
    print("test() called")
    return "Hello from Server!"

# check if the executed file is the main program
if __name__ == "__main__":
    app.run(port=5000) # run the app
