from flask_app import app

from flask_app.controllers import users,recipes,places

if __name__=="__main__":
    app.run(debug=True)