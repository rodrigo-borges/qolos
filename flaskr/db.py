import click

from flask import current_app, g
from flask.cli import with_appcontext

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flaskr.models import Base


def get_engine():

	engine = create_engine(current_app.config["DATABASE"])
	return engine


def get_db():

	if "db" not in g:
		engine = get_engine()
		Session = sessionmaker(bind=engine)
		g.db = Session()

	return g.db


def close_db(e=None):

	db = g.pop("db", None)

	if db is not None:
		db.close()


def init_db():

	engine = get_engine()
	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)


@click.command("init-db")
@with_appcontext
def init_db_command():
	"""Clear the existing data and create new tables"""
	init_db()
	click.echo("Initialized the database.")


def init_app(app):
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)