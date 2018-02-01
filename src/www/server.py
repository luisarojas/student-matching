from flask import Flask
from flask import render_template, request, json
from werkzeug import secure_filename

#Global Variables
UPLOAD_FOLDER="./src/www/uploads/"

#Define the app
app = Flask(__name__)

#APP configurations
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def queryDB(query):
    # get data from container
    import psycopg2 as pg

    db = pg.connect(dbname="db",
                    host="localhost",
                    user="myuser",
                    password="secret")

    c = db.cursor()
    c.execute(query)

    all_entries = []
    for row in c.fetchall():
        all_entries.append(row)

    # Close communication with the database
    c.close()
    db.close()

    return all_entries

# define basic route
@app.route("/")
def printData():
    return render_template('data.html', title="Mentor Mentee Matching")

	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'

# triggered on start up
@app.route("/test", methods=['GET'])
def test():
    print("test() called")
    return "Hello from Server!"

# check if the executed file is the main program
if __name__ == "__main__":
    app.run(port=5000) # run the app
