# gtm_flask

This is a subscription management app for an email newsletter.

This was setup largely using[this](https://realpython.com/blog/python/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/)guide. 

It contains two special branches linked to Heroku accounts:
* staging
* production

Do your work in master and simply push to staging or production to deploy.

## Database Migrations

If you omake changes to the local ORM, you'll need to reflect them in the database.
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