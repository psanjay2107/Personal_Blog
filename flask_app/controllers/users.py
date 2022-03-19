from flask import render_template,redirect,session,request, flash,url_for
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_app.models.place import Place
from flask_bcrypt import Bcrypt
import os
import urllib.request
from werkzeug.utils import secure_filename
bcrypt = Bcrypt(app)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_image(dir):
    if 'foodblog_img' not in request.files:
        flash('No file part')
        return redirect(request.url)
    if 'travelblog_img' not in request.files:
        flash('No file part')
        return redirect(request.url)
    if 'profile_img' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file1 = request.files['foodblog_img']
    file2 = request.files['travelblog_img']
    file3 = request.files['profile_img']
    
    if file1 and allowed_file(file1.filename):
        mode = 0o777
        basedir = os.path.abspath(os.path.dirname(__file__))
        filename = secure_filename(file1.filename)
        print('####################### dirname: ' + filename)
        filename = dir+'food'+'.png'
        print('####################### dirname: ' + filename)
        if not os.path.exists (os.path.join(basedir, app.config['UPLOAD_FOLDER_USER'], dir, filename)):
            os.mkdir(os.path.join(basedir, app.config['UPLOAD_FOLDER_USER'], dir), mode)
        file1.save(os.path.join(basedir, app.config['UPLOAD_FOLDER_USER'], dir, filename))
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('####################### dirname: ' + basedir)
        #print('####################### data: ' + dir)
        flash('Image successfully uploaded and displayed below')
        if 'user_id' not in session:
            return redirect('/logout')
            data ={
                'id': session['user_id']
            }
            return render_template("foodblog.html",user=User.get_by_id(data),filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

    if file2 and allowed_file(file2.filename):
        mode = 0o777
        basedir = os.path.abspath(os.path.dirname(__file__))
        filename = secure_filename(file2.filename)
        print('####################### dirname: ' + filename)
        filename = dir+'travel'+'.png'
        print('####################### dirname: ' + filename)
        if not os.path.exists (os.path.join(basedir, app.config['UPLOAD_FOLDER_USER'], dir)):
            os.mkdir(os.path.join(basedir, app.config['UPLOAD_FOLDER_USER'], dir), mode)
        file2.save(os.path.join(basedir, app.config['UPLOAD_FOLDER_USER'], dir, filename))
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('####################### dirname: ' + basedir)
        #print('####################### data: ' + dir)
        flash('Image successfully uploaded and displayed below')
        if 'user_id' not in session:
            return redirect('/logout')
            data ={
                'id': session['user_id']
            }
            return render_template("foodblog.html",user=User.get_by_id(data),filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)
    
    if file3 and allowed_file(file3.filename):
        mode = 0o777
        basedir = os.path.abspath(os.path.dirname(__file__))
        filename = secure_filename(file3.filename)
        print('####################### dirname: ' + filename)
        filename = dir+'profile'+'.png'
        print('####################### dirname: ' + filename)
        if not os.path.exists (os.path.join(basedir, app.config['UPLOAD_FOLDER_USER'], dir)):
            os.mkdir(os.path.join(basedir, app.config['UPLOAD_FOLDER_USER'], dir), mode)
        file3.save(os.path.join(basedir, app.config['UPLOAD_FOLDER_USER'], dir, filename))
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('####################### dirname: ' + basedir)
        #print('####################### data: ' + dir)
        flash('Image successfully uploaded and displayed below')
        if 'user_id' not in session:
            return redirect('/logout')
            data ={
                'id': session['user_id']
            }
            return render_template("foodblog.html",user=User.get_by_id(data),filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.add_user(data)
    session['user_id'] = id

    return redirect('/user_page')

@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/user_page')

@app.route('/user_page')
def user_page():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("user_page.html",user=User.get_by_id(data),lst=User.get_all())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/foodblog')
def food_blog():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("foodblog.html",user=User.get_by_id(data))

@app.route('/travelphotoblog')
def travel_and_photo_blog():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("travel_photo.html",user=User.get_by_id(data))

@app.route('/write_about')
def about_yourself():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("About.html",user=User.get_by_id(data))

@app.route('/update_about/<fname>/<lname>',methods=['POST'])
def update_about_yourself(fname,lname):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id'],
        "about_me": request.form["about_me"],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    
    dir_name = fname + lname + str(session['user_id'])

    upload_image(dir_name)
    User.about(data)
    #print(dir_name)
    return redirect('/user_page')
    #return render_template("About.html",user=User.get_by_id(data))

@app.route('/home/aboutme')
def about_me():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id'],
    }
    #return redirect('/user_page')
    return render_template("About_me.html",user=User.get_by_id(data))


@app.route('/show_blog/<int:id>')
def show_blog(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("show_blog.html",recipes=Recipe.get_by_id(data),user=User.get_by_id(data),places=Place
    .get_by_id(data))