# gtm_flask

This is a subscription management app for an email newsletter.

This was setup largely using [this](https://realpython.com/blog/python/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/) guide. 

It contains two special branches linked to Heroku accounts:
* staging
* production

Do your work in master and simply push to staging or production to deploy.

## Running the application locally

To run the app locally, create a new config file called "config_local.py" in the project root directory.  It should contain a class called DevelopmentConfig and inherit from config.Config
```
from config import Config


class DevelopmentConfig(Config):
    NAME = "DEVELOPMENT"
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/gtm_development" 
```

Finally, use this terminal command

`export environment=config_local.DevelopmentConfig && python app.py`

Note that this file is in the `.gitignore` so you can put API keys here 

### First time running in any environment

The first time you run the app, you'll need to bootstrap the database with the default user.  To do that, simply hit this URL:`localhost:5000/bootstrap`

### Running Tests

Use the following command in the `gtm_flask` directory to run tests:

`export environment=config.TestingConfig && nosetests`

## Database Migrations

If you make changes to the local ORM, you'll need to reflect them in the database.
To do so, run the following commands: 
```
python manage.py db migrate
python manage.py db upgrade
```

When you're ready to push your changes to staging/prod, do so.

Then run:
```
heroku run python manage.py db upgrade --app APP_NAME_HERE
```
This will apply the changes you made locally to the Heroku Postgres