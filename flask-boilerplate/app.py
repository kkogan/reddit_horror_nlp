# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import flask
from flask import Flask, render_template, request

# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import numpy as np
import pandas as pd

# ---------- MODEL IN MEMORY ----------------#

# Read the scientific data on breast cancer survival,
# Build a LogisticRegression predictor on it
reddit = pd.read_pickle("../../resources/pickles/scores_df.pkl")

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object("config")
# db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
"""
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
"""

# Login required decorator.
"""
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
"""
# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#
topics = [
    "Subtle Cues",
    "True Confessional",
    "Experimental Facility",
    "Newborn Child",
    "Wilderness",
    "Automotive",
    "In The House",
    "Violent Action",
    "Bones & Flesh",
    "Medical",
    "Technology",
    "Party Hard",
    "Neighborhood",
    "Food",
    "Night Terrors",
    "Family",
    "What Was That Sound?",
    "Evil Spirit",
    "Schools Out Forever",
    "The Ocean",
    "Contemplation",
    "Crime & Punishment",
]


@app.route("/")
def home():
    return render_template("pages/placeholder.home.html")


@app.route("/filter", methods=["POST"])
def score():
    """
    When A POST request with json data is made to this uri,
    Read the example from the json, predict probability and
    send it with a response
    """
    # Get decision score for our example that came with the request
    print(flask.request.json)
    data = flask.request.json
    # x = np.matrix(data["example"])
    # score = PREDICTOR.predict_proba(x)
    # Put the result in a nice dict so we can send it as json
    # topic_filter=['Newborn Child']
    topic_filter = data["topics"]
    top_n = 10

    # results = {"score": 60, "title":'scary', 'link':'https://reddit.com/r/nosleep'}
    # results = reddit[['score','title','full_link']].sort_values(by=['score'], ascending=False).head(5).to_json(orient='records')
    # results = reddit.assign(f = reddit[topic_filter].sum()*reddit['score']).sort_values('f', ascending=False).drop('f', axis=1).head(5).to_json(orient='records')
    df = (
        reddit.assign(
            topic_score=(0.001 + reddit[topic_filter].sum(axis=1))
            * np.log(reddit["score"])
        )
        .sort_values("topic_score", ascending=False)
        .head(top_n)
    )
    df
    res = df[["score", "topic_score", "title", "full_link", "1+2+3"]].to_json(
        orient="records"
    )
    # return flask.jsonify(results)
    return res


@app.route("/about")
def about():
    return render_template("pages/placeholder.about.html")


@app.route("/login")
def login():
    form = LoginForm(request.form)
    return render_template("forms/login.html", form=form)


@app.route("/register")
def register():
    form = RegisterForm(request.form)
    return render_template("forms/register.html", form=form)


@app.route("/forgot")
def forgot():
    form = ForgotForm(request.form)
    return render_template("forms/forgot.html", form=form)


# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template("errors/500.html"), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == "__main__":
    app.run()

# Or specify port manually:
"""
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
"""
