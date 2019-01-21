from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
from helpers import check_win, minimax

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

    # Check for winner
    session["winner"] = check_win(session["board"], session["turn"])

    # next move
    if session["turn"] == "X":
        session["turn"] = "O"
    else:
        session["turn"] = "X"

    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    try:
        del(session["board"])
    except KeyError:
        pass
    return redirect(url_for("index"))

@app.route("/ai")
def ai():
    # Manual copy of session["board"]! Using session["board"].copy(), 
    # list(session["board"]), and session["board"][:] didn't work!
    # All return a session object.
    game = [[None, None, None], [None, None, None], [None, None, None]]
    for i in range(3):
        for j in range(3):
            game[i][j] = session["board"][i][j]
    turn = str(session["turn"])
    move = minimax(game, turn)
    return redirect(url_for("play", row=move[1][0], col=move[1][1]))
