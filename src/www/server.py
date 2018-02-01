from flask import Flask
from flask import render_template, request, json
from werkzeug import secure_filename
from os import path

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

	
@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
    print("uploader() called")
    print("files:", request.files["file"])
    if request.method == "POST":
        #Ensure that the request has the file part
        if "file" not in request.files:
            print("ERROR:", "post request missing file part")
            return redirect(request.url)

        client_file = request.files["file"]
        #Check if request was submitted without a file
        if client_file.filename == "":
            print("ERROR:", "User did not attach a file")
            return redirect(request.url)

        #Actually submitted a file
        if client_file and allowed_file(client_file.filename):
            filename  = secure_filename(client_file.filename)
            client_file.save(path.join(app.config['UPLOAD_FOLDER'], filename))
            return "UPLOAD SUCCESS"
    return "UPLOAD UNSUCCESSFUL"

# def upload_file():
#    if request.method == 'POST':
#       f = request.files['file']
#       f.save(secure_filename(f.filename))
#       return 'file uploaded successfully'

# triggered on start up
@app.route("/test", methods=['GET'])
def test():
    print("test() called")
    return "Hello from Server!"

# check if the executed file is the main program
if __name__ == "__main__":
    app.run(port=5000) # run the app
