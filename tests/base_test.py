from flask_testing import TestCase

from run import db, create_app


class MyTest(TestCase):

    def create_app(self):

        app = create_app()
        db.init_app(app)

        if not app.config.get("TESTING"):
            raise Exception("Cannot run tests unless in test mode")
        return app

    def setUp(self):

        db.create_all()

    def tearDown(self):

        db.session.remove()
        db.drop_all()
