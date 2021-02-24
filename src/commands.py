from main import db
from flask import Blueprint
from werkzeug.security import generate_password_hash


db_commands = Blueprint("db-custom", __name__)


@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")


@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("Tables deleted")


@db_commands.cli.command("seed")
def seed_db():
    from models.User import User
    from models.Journal import Journal

    u1 = User()
    u1.email = "pandeli@test.com"
    u1.name = "Pandelis"
    u1.password = generate_password_hash("password", method='sha256')
    db.session.add(u1)
    db.session.commit()
    print("User table seeded")

    journal = Journal()
    journal.journal_entry = "Test Entry from seeding"
    journal.user_id_fk = 1
    db.session.add(journal)
    db.session.commit()
    print("Journal table seeded")
