# DEFINES THE FLASK APLICATION SETTINGS AND INCLUDES SOME TASKS THAT HELP MANAGE THE APPLICATION
import os
from app import create_app, db
from app.model import Event, WebSource
from flask_migrate import Migrate

app = create_app(os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Event=Event, WebSource=WebSource)


### IN SHELL ###
# $ pip install -r requirements.txt
# $ export FLASK_APP = events_app.py
# $ export FLASK_DEBUG = 1
# $ flask run

### DB ###
# $ flask db init
# $ flask db migrate -m 'initial migration'
# $ flask db upgrade (once a migration script has been accepted, it can be applied to the database using this command)
# $ db.create_all()

### FLASK SHELL ###

# $ flask shell
# $ app
# $ db
# $ Event
