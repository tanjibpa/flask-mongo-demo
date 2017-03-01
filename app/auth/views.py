import bcrypt
from functools import wraps
from flask import request, redirect, url_for, render_template, session, flash
from . import auth
from .forms import LoginForm
import pymongo

client = pymongo.MongoClient('mongodb://tanjib:devilsass@localhost:27017/')
db = client['journo']
collection = db['journo']


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        else:
            flash('Please log in first.')
            return redirect(url_for('main.index'))
    return wrap

@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            users = collection.users
            login_user = users.find_one({'username': form.username.data})
            print(login_user)

            if login_user:
                if bcrypt.checkpw(form.password.data.encode('utf-8'), login_user['password']):
                    session['username'] = request.form['username']
                    return redirect(url_for('main.index'))
            return 'Invalid username/password'
    else:
        return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = collection.users
        if users.find_one({'username': request.form['username']}) is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'username': request.form['username'], 'password': hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('main.index'))
        return 'That username already exist'
    return render_template('auth/register.html')


@auth.route('/logout')
def logout():
    if 'username' in session:
        del session['username']
        return redirect(url_for('main.index'))
    return redirect(url_for('main.index'))