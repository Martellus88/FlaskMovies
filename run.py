import os
from app import create_app, db
from flask_migrate import Migrate
from app.models import User, Movies

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def shell_context():
    return dict(db=db, User=User, Movies=Movies)