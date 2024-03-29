"""Script to seed DB"""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

server.app.app_context().push()

os.system("dropdb ratings")
os.system("createdb ratings")

model.connect_to_db(server.app)
model.db.create_all()


with open('data/movies.json') as f:
    movie_data = json.loads(f.read())


movies_db = []

for movie in movie_data:
    release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")
    db_movie = crud.create_movie(title=movie["title"], overview=movie["overview"], release_date=release_date, poster_path=movie["poster_path"])
    movies_db.append(db_movie)


model.db.session.add_all(movies_db)
model.db.session.commit()

for n in range(10):
    email = f"user{n}@test.com"  # Voila! A unique email!
    password = "test"

    user = crud.create_user(email, password)
    model.db.session.add(user)

    for _ in range(10):
        random_movie = choice(movies_db)
        score = randint(1, 5)

        rating = crud.create_rating(score, random_movie, user)
        model.db.session.add(rating)

model.db.session.commit()