import os
import urllib.request
from flask import render_template,redirect,session,request, flash,url_for
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_image(dir):
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
        if not os.path.exists (os.path.join(basedir, app.config['UPLOAD_FOLDER_RECIPE'], dir, filename)):
            os.mkdir(os.path.join(basedir, app.config['UPLOAD_FOLDER_RECIPE'], dir), mode)
        file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER_RECIPE'], dir, filename))
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

@app.route('/new/recipe')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_recipe.html',user=User.get_by_id(data))

@app.route('/home/recipe')
def nav_home():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('foodblog.html',user=User.get_by_id(data))

@app.route('/recipes')
def list_of_recipes():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }

    return render_template("recipes_list.html",user=User.get_by_id(data),recipes=Recipe.get_all(),lst=User.get_all())

@app.route('/recipe/<int:id>')
def show_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("show_recipe.html",recipe=Recipe.get_one(data),user=User.get_by_id(user_data))

@app.route('/dashboard')
def nav_user_page():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('user_page.html',user=User.get_by_id(data))

@app.route('/create/recipe',methods=['POST'])
def create_recipe():
        if 'user_id' not in session:
            return redirect('/logout')
        if not Recipe.validate_recipe(request.form):
            return redirect('/new/recipe')
		
        data = {
            "title": request.form["title"],
            "instructions": request.form["instructions"],
            "time": request.form["time"],
            "user_id": session["user_id"]
        }
        Recipe.add_recipe(data)
        upload_image(request.form["title"])
        return redirect('/recipes')

@app.route('/update/recipe',methods=['POST'])
def update_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/new/recipe')
    data = {
        "title": request.form["title"],
        "time": request.form["time"],
        "instructions": request.form["instructions"],
        "id": request.form['id']
    }
    Recipe.update(data)
    return redirect('/recipes')

@app.route('/edit/recipe/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    
    return render_template("edit_recipe.html",edit=Recipe.get_one(data),user=User.get_by_id(user_data))

@app.route('/destroy/recipe/<int:id>')
def destroy_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Recipe.destroy(data)
    return redirect('/recipes')

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)