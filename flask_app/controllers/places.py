import os
import urllib.request
from flask import render_template,redirect,session,request, flash,url_for
from flask_app import app
from flask_app.models.place import Place
from flask_app.models.user import User
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_image_travel(dir):
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        mode = 0o777
        basedir = os.path.abspath(os.path.dirname(__file__))
        filename = secure_filename(file.filename)
        #print('####################### dirname: ' + filename)
        filename = dir+'.png'
        print('####################### dirname: ' + filename)
        if not os.path.exists (os.path.join(basedir, app.config['UPLOAD_FOLDER_TRAVEL'], dir, filename)):
            os.mkdir(os.path.join(basedir, app.config['UPLOAD_FOLDER_TRAVEL'], dir), mode)
            file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER_TRAVEL'], dir, filename))
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('####################### dirname: ' + basedir)
        #print('####################### data: ' + dir)
        flash('Image successfully uploaded and displayed below')
        if 'user_id' not in session:
            return redirect('/logout')
            data ={
                'id': session['user_id']
            }
            return render_template("travel_photo.html",user=User.get_by_id(data),filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/home/travel')
def nav_home_travel():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('travel_photo.html',user=User.get_by_id(data))

@app.route('/places')
def nav_places():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('places_list.html',user=User.get_by_id(data),places=Place.get_all(),lst=User.get_all())

@app.route('/new/place')
def nav_new_place():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('add_place.html',user=User.get_by_id(data))

@app.route('/create/place',methods=['POST'])
def create_place():
        if 'user_id' not in session:
            return redirect('/logout')
        #if not Recipe.validate_recipe(request.form):
        #    return redirect('/new/recipe
		
        data = {
            "location": request.form["location"],
            "description": request.form["description"],
            "date": request.form["date"],
            "users_id": session["user_id"]
        }
        Place.add_place(data)
        upload_image_travel(request.form["location"])
        return redirect('/places')

@app.route('/place/<int:id>')
def show_place(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("show_place.html",place=Place.get_one(data),user=User.get_by_id(user_data))

@app.route('/destroy/place/<int:id>')
def destroy_place(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Place.destroy(data)
    return redirect('/places')

@app.route('/update/place',methods=['POST'])
def update_place():
    if 'user_id' not in session:
        return redirect('/logout')
    #if not Recipe.validate_recipe(request.form):
    #    return redirect('/new/recipe')
    data = {
        "location": request.form["location"],
        "date": request.form["date"],
        "description": request.form["description"],
        "id": request.form['id']
    }
    Place.update(data)
    return redirect('/places')

@app.route('/edit/place/<int:id>')
def edit_place(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    
    return render_template("edit_place.html",edit=Place.get_one(data),user=User.get_by_id(user_data))