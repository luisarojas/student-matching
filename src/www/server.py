from flask import Flask
from flask import render_template, request, json

app = Flask(__name__)

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

# triggered on start up
@app.route("/test", methods=['GET'])
def test():
    print("test() called")
    return "Hello from Server!"

# check if the executed file is the main program
if __name__ == "__main__":
    app.run(port=5000) # run the app
