from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_app.models.place import Place
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

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

@app.route('/update_about',methods=['POST'])
def update_about_yourself():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id'],
        "about_me": request.form["about_me"]
    }
    User.about(data)
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