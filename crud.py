""" CRUD Operations """

from model import db, User, Movie, Rating, connect_to_db

#functions: 

def create_user(email, password):
    """Create and return a new user"""
    user = User(email=email, password=password)
    return user


def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie."""
    movie = Movie(title=title, overview=overview, release_date=release_date, poster_path=poster_path)
    return movie


def create_rating(score, movie, user):
    """Create and return a new rating"""
    rating = Rating(score=score, movie=movie, user=user)
    return rating


def get_movies():
    """Return all movies"""
    return Movie.query.all()

def get_movie_by_id(id):
    """Return a movie by its ID"""
    return Movie.query.get(id)

def get_users():
    """return all users"""
    return User.query.all()

def get_user_by_id(id):
    """return user by ID"""
    return User.query.get(id)

def get_user_by_email(email):
    """return user by email"""
    return User.query.filter(User.email == email).first()

def get_ratings_by_movie(movie_id):
    """returns all ratings of a certain movie"""
    return Rating.query.filter(Rating.movie_id == movie_id).all()

if __name__ == "__main__":
    from server import app
    connect_to_db(app)