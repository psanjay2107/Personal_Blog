from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class Recipe:
    db = "login_reg"
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.instructions = data['instructions']
        self.time = data['time']
        self.user_id = data['user_id']
        self.image_name = data['image_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def add_recipe(cls,data):
        query = "INSERT INTO recipe (title,instructions,time,user_id) VALUES(%(title)s,%(instructions)s,%(time)s,%(user_id)s)"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipe;"
        results =  connectToMySQL(cls.db).query_db(query)
        all_recipes = []
        for row in results:
            #print(row['date_made'])
            all_recipes.append( cls(row) )
        return all_recipes

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM recipe WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls( results[0] )
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM recipe WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def update(cls, data):
        query = "UPDATE recipe SET title=%(title)s, time=%(time)s, instructions=%(instructions)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM recipe WHERE user_id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        all_recipe = []
        for row in results:
            #print(row['date_made'])
            all_recipe.append( cls(row) )
        return all_recipe