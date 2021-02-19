from flask_login import UserMixin
from main import db
from flask_seeder import Seeder, Faker, generator

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


# All seeders inherit from Seeder
class DemoSeeder(Seeder):

  # run() will be called by Flask-Seeder
  def run(self):
    # Create a new Faker and tell it how to create User objects
    faker = Faker(
      cls=User,
      init={
        "id": generator.Sequence(),
        "email": generator.Email(),
        "name": generator.Name(),
        "password": "testing"
      }
    )

    # Create 5 users
    for user in faker.create(5):
      print("Adding user: %s" % user)
      self.db.session.add(user)