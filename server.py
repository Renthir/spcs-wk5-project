"""Server for movie ratings app."""

from flask import Flask, render_template, redirect, request, flash, url_for, session
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined

#route functions

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/users', methods=["GET"])
def users():
    users = crud.get_users()
    return render_template('users.html', users=users)

@app.route('/users', methods=["POST"])
def new_user():
    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)
    if user:
        flash("Email already taken")
    else:
        user = crud.create_user(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")
    return redirect("/")

@app.route('/users/<user_id>')
def user_details(user_id):
    user = crud.get_user_by_id(user_id)
    return render_template('user_details.html', user=user)

@app.route('/movies')
def movies():
    movies = crud.get_movies()
    return render_template('movies.html', movies=movies)

@app.route('/movies/<movie_id>')
def movie_details(movie_id):
    movie = crud.get_movie_by_id(movie_id)
    ratings = crud.get_ratings_by_movie(movie_id)
    scores = [rating.score for rating in ratings]
    avg_score  = sum(scores) / len(scores)
    return render_template('movie_details.html', movie=movie, ratings=ratings, avg_score=avg_score)

@app.route('/login', methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)
    if user.password == password:
        session['user_id'] = user.user_id
        flash('Logged In!')
    else:
        flash("Invalid login information")
    return redirect('/')

@app.route('/rate/<movie_id>')
def rate_movie(movie_id):
    movie = crud.get_movie_by_id(movie_id)
    return render_template('rate_movie.html', movie=movie)

@app.route('/rate/<movie_id>', methods=["POST"])
def rate_form(movie_id):
    score = request.form.get("rating")
    movie = crud.get_movie_by_id(movie_id)
    if session.get("user_id") != None:
        user = crud.get_user_by_id(session["user_id"])
        rating = crud.create_rating(score, movie, user)
        db.session.add(rating)
        db.session.commit()
        return redirect(f'/movies/{movie_id}')
    else:
        flash("Please Log in")
        return redirect('/')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
