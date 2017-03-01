import os
from flask import render_template, redirect, session, current_app, flash, send_file, url_for
from . import main
from .forms import InputForm
from werkzeug.utils import secure_filename
from ..auth import login_required
import pymongo

client = pymongo.MongoClient('mongodb://tanjib:devilsass@localhost:27017/')
db = client['journo']
collection = db['journo']


@main.route('/')
def index():
    if 'username' in session:
        return render_template('main/index.html')
    return render_template('main/index.html')


@main.route('/input_area', methods=['POST', 'GET'])
@login_required
def input_area():
    form = InputForm()
    if form.validate_on_submit():
        files = collection.files
        name = form.name.data
        email = form.email.data
        f = form.upload_file.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(current_app.root_path, 'files', filename))
        files.insert({
            'username': session['username'], 
            'name': name, 
            'email': email,
            'filename': filename})
        flash('File uploaded successfully!')
        return redirect('/')
    return render_template('main/input_area.html', form=form)


@main.route('/all_info')
@login_required
def all_info():
    files = collection.files.find()
    return render_template('main/all-info.html', files=files)


@main.route('/download_file/<filename>')
@login_required
def download_file(filename):
    if os.path.isfile(os.path.join(current_app.root_path, 'files', filename)):
        return send_file(os.path.join(current_app.root_path, 'files', filename))
    flash('File does not exist.')
    return redirect(url_for('main.all_info'))

