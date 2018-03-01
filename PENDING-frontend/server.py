from flask import Flask, render_template, request

app = Flask(__name__)

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
