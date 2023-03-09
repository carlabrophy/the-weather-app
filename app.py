from flask import Flask, render_template, redirect, flash, session
from models import db, connect_db, User, Weather
from forms import UserForm, WeatherForm
from flask_debugtoolbar import DebugToolbarExtension
from secret import API_SECRET_KEY, APP_CONFIG_KEY
from sqlalchemy.exc import IntegrityError
import requests, datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///weather_planner_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

db.create_all()

app.config['SECRET_KEY'] = APP_CONFIG_KEY
debug = DebugToolbarExtension(app)


BASE_URL = f"https://api.tomorrow.io/v4/weather/forecast?"
headers = {"accept": "application/json"}

# params={'key': API_SECRET_KEY, 'location': '', 'timesteps': '1d', 'units': 'imperial'}



def fetch_data(location, date_input):
    loc = location
    response = requests.get(BASE_URL, headers=headers, params={'location': loc, 'timesteps': '1d', 'units': 'imperial', 'apikey': API_SECRET_KEY})

    data = response.json()

    for daily in data['timelines']['daily']:
        time = daily['time']
        date = time[5:-10]

        if date == date_input:
            temp = daily['values']['temperatureAvg']
            description = daily['values']['weatherCodeMax']
            humidity = daily['values']['humidityAvg']

            new_weather = {'temperature': temp, 'description': description, 'humidity': humidity}
            return new_weather
        
    

@app.route('/')
def show_homepage():
    """Show hompage"""
    return render_template('index.html')



@app.route('/register', methods=['GET', 'POST'])
def show_register_form():
    """Show log in form and handle requests"""
    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        new_user = User.register(username, password)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username is not available.')
            return render_template('register.html', form=form)
        
        #add the user_id in the seesion right away so user don't have to log in again after registering on the account.
        session['user_id'] = new_user.id
        flash(f'Welcome {username}! Your account has been created.', 'success')
        return redirect(f'/user')
    else:
        return render_template('register.html', form=form)
    



@app.route('/login', methods=['GET','POST'])
def user_login():

    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['user_id'] = user.id
            flash(f'Welcome back {username}!', 'info')
            return redirect('/posts')
        else:
            form.username.errors = ['Incorrect username/password']

    
    return render_template('login.html', form=form)





@app.route('/user', methods=['GET', 'POST'])
def show_weather_forms():
    """Show weather forms but authenticate if use ris log in first"""

    if 'user_id' not in session:
        flash('Please log in first.', 'danger')
        return redirect('/')

    form = WeatherForm()
    l_weathers = Weather.query.filter_by(user_id=session['user_id'], column='left').all()
    r_weathers = Weather.query.filter_by(user_id=session['user_id'], column='right').all()


    if form.validate_on_submit():
        address = form.location.data
        date = form.date.data
        column = form.column.data

        weather = fetch_data(address,date)

        new_weather = Weather(date=date, location=address, temperature=weather['temperature'], description=weather['description'], humidity=weather['humidity'], user_id=session['user_id'], column=column)

        db.session.add(new_weather)
        db.session.commit()
        return redirect('/user')

    else:
       
        return render_template('user.html', form=form, l_weathers=l_weathers, r_weathers=r_weathers)






@app.route('/weather/<int:id>/edit', methods=['GET', 'POST'])
def edit_weather(id):
    """Edit a weather info"""

    form = WeatherForm()
    w = Weather.query.get_or_404(id)

    if form.validate_on_submit():
        date = form.date.data
        location = form.location.data

        weather = fetch_data(location,date)

        w.date = date
        w.location = location
        w.temperature = weather['temperature']
        w.description = weather['description']
        w.humidity = weather['humidity']

        db.session.commit()
        return redirect('/user')
    
    else:
        return render_template('edit_weather.html', form=form)
    


    
@app.route('/weather/<int:id>/delete')
def delete_weather(id):
    """delete a weather"""
    w = Weather.query.get_or_404(id)

    db.session.delete(w)
    db.session.commit()

    return redirect('/user')

    



@app.route('/logout')
def logout():
    """logout user and remove user_id from session"""
    session.pop('user_id')

    return redirect('/')






    
    
          
    
        