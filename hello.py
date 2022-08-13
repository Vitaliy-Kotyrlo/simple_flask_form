from flask import Flask, request, jsonify, abort, redirect, url_for, render_template, send_file, flash
from markupsafe import escape
from joblib import dump, load
import numpy as np
import pandas as pd
knn = load('knn.pkl')
app = Flask(__name__)
import os
def mean(n):
    return(float(sum(n))/max(len(n),1))

     

@app.route("/")
def hello_world():
    print("hi")
    return "<p>Wordfghsdfgfasdfgsafafrea2232324dsjhgfdld!</p>"

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    username = float(username)*float(username)
    return f'User {escape(username)}'

@app.route('/avg/<nums>')
def show_user_avf(nums):
    nums = nums.split(',')
    nums = [float(i) for i in nums]
    nums_mean = mean(nums)
    return f'{escape(nums_mean)}'


@app.route('/iris/<param>')
def iris(param):

    param = param.split(',')
    param = [float(i) for i in param]
    param = np.array(param).reshape(1,-1)
    print(param)
    # iris_y_test
    pred = knn.predict(param)
    return f'{escape(pred)}'

@app.route('/show_image')
def show_image():
    return '<img src="static/setosa.jpg" alt="setosa">'

@app.route('/iris_post', methods=['POST'])
def add_message():
    try:
        content = request.get_json()
        print(content)
        param = content['flower'].split(',')
        param = [float(i) for i in param]
        param = np.array(param).reshape(1,-1)
        print(param)
        # iris_y_test
        pred = knn.predict(param)
        pred = {'class':str(pred[0])}
    except:
        return redirect(url_for('bad_request'))
    return jsonify(pred)

@app.route('/badrequest400')
def bad_request():
    return abort(400)

from flask_wtf import FlaskForm
from wtforms import StringField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    file = FileField(validators=[FileRequired()])

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = MyForm()
    
    if form.validate_on_submit():
        print(form.name.data )
        f = form.file.data
        filename = form.name.data + '.csv'
        # # filename = secure_filename(f.filename)
        # f.save(os.path.join(
        #     filename
        # ))
        df = pd.read_csv(f, header = None)
        print(df.head)
        pred = knn.predict(df)
        print(pred)
        pd.DataFrame(pred).to_csv(filename, index = False)

        return send_file(
            filename,
            mimetype='text/csv',
            download_name=filename,
            as_attachment=True
                )

        # return (str(form.name))
        # return redirect('/success')
    return render_template('submit.html', form=form)

# @app.route('/template', methods=['GET', 'POST'])
# def template():
#     if request.method == 'POST':
#         return "Hello"
#     return render_template('index.html')


import os
# from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename + 'uploaded')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'file uploaded'
            # return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''