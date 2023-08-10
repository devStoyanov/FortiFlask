from flask.cli import FlaskGroup

from project import create_app
from project.models import db

app = create_app()

# Create a new FlaskGroup instance to extend the normal CLI with
# commands related to the Flask app.
cli = FlaskGroup(app)


# Configure the Flask CLI tool to
# run and manage the app from the command line
@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    cli()
