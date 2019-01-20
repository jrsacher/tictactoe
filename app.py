from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():

    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"
        session["winner"] = None

    return render_template("game.html", game=session["board"], turn=session["turn"], winner=session["winner"])

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    # add move
    session["board"][row][col] = session["turn"]

    # Check for win
    # Check rows and columns
    for i in range(3):
        if ((session["board"][i][0] == session["turn"] and 
            session["board"][i][1] == session["turn"] and
            session["board"][i][2] == session["turn"]) or 
            (session["board"][0][i] == session["turn"] and
            session["board"][1][i] == session["turn"] and
            session["board"][2][i] == session["turn"])):
            session["winner"] = session["turn"]
            break
    # Check diagonals
    if ((session["board"][0][0] == session["turn"] and
        session["board"][1][1] == session["turn"] and
        session["board"][2][2] == session["turn"]) or 
        (session["board"][0][2] == session["turn"] and
        session["board"][1][1] == session["turn"] and
        session["board"][2][0] == session["turn"])):
       session["winner"] = session["turn"]

    # next move
    if session["turn"] == "X":
        session["turn"] = "O"
    else:
        session["turn"] = "X"

    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    del(session["board"])
    return redirect(url_for("index"))
