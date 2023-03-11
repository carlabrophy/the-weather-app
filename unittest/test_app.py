from unittest import TestCase
from secret import API_SECRET_KEY, APP_CONFIG_KEY
from app import app
from models import db, connect_db, User, Weather
from forms import UserForm
from flask import session


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///weather_db_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.create_all()

class HompageTestCase(TestCase):


    def test_homepage(self):

        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<a href="/login" class="btn btn-success">Log in</a>', html)
    


class RegisterTestCase(TestCase):


    def test_register(self):

        with app.test_client() as client:

            res = client.get('/register')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<button type="submit" class="btn btn-success">Submit</button>', html)
            



    def test_register_post(self):

        with app.test_client() as client:

            res = client.post('/register', data={'username': 'cassiegirl'})
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<input id="username" name="username" required type="text" value="cassiegirl">', html)



    def test_register_session(self):

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['user_id'] = 3

            res = client.get('/register')

            self.assertEqual(res.status_code, 200)
            self.assertEqual(session['user_id'], 3)
        

    


class LoginTestCase(TestCase):
       
    def test_login(self):

        with app.test_client() as client:

            res = client.get('/login')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<button type="submit" class="btn btn-success">Submit</button>', html)

    

    def test_login_post(self):

        with app.test_client() as client:

            res = client.post('/login', data={'username': 'bambam'}, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<input id="username" name="username" required type="text" value="bambam">', html)

    

    def test_login_session(self):

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['user_id'] = 2

            res = client.get('/login', follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(session['user_id'], 2)




class UserTestCase(TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()
        user = User.register('cassiegirl', 'ilovebambam')
        db.session.add(user)
        db.session.commit()


    def tearDown(self):
        db.session.rollback()

    def test_user(self):
        with app.test_client() as client:

            res = client.get('/user', follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Welcome to Weather Planner.</h1>', html)



    
    def test_user_post(self):

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['user_id'] = 1

            res = client.post('/user', data={'location': 'newyork', 'date': '03-11', 'column': 'left' , 'user_id':change_session['user_id']}, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<input id="location" name="location" placeholder="newyork" required type="text" value="">', html)
                            


    def test_user_session(self):

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['user_id'] = 2

            res = client.get('/user', follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(session['user_id'], 2)





class WeatherTestCase(TestCase):

    def setUp(self):
            db.drop_all()
            db.create_all()
            user = User.register('cassiegirl', 'ilovebambam')

            self.user_id = user.id
            weather  = Weather(date='08-12', location='newyork', temperature=64.31, description='1000', humidity=60.10, user_id=self.user_id, column='left' )
            db.session.add(user)
            db.session.add(weather)
            db.session.commit()

            


    def tearDown(self):
            db.session.rollback()



    def test_weather_edit(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                    change_session['user_id'] = 1
            
            res = client.get(f'/weather/{change_session["user_id"]}/edit')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<input id="location" name="location" placeholder="newyork" required type="text" value="">', html)
            

    
    def test_weather_delete(self):

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                    change_session['user_id'] = 1

        res = client.get(f'/weather/{change_session["user_id"]}/delete', follow_redirects=True)
        html = res.get_data(as_text=True)

        self.assertEqual(res.status_code, 200)
        self.assertIn('<label for="column">Choose which table:</label>', html)

    

    def test_logout(self):

         with app.test_client() as client:
            with client.session_transaction() as change_session:
                    change_session['user_id'] = None

            res = client.get('/logout', follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(change_session['user_id'], None)
       