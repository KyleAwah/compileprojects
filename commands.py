import click
from flask.cli import with_appcontext
from models import db, user, product, orders, wish_list
from main import app
import psycopg2

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()
