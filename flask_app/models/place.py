from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class Place:
    db = "login_reg"
    def __init__(self,data):
        self.id = data['id']
        self.location = data['location']
        self.description = data['description']
        self.date = data['date']
        self.users_id = data['users_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def add_place(cls,data):
        query = "INSERT INTO places (location,description,date,users_id) VALUES(%(location)s,%(description)s,%(date)s,%(users_id)s)"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM places;"
        results =  connectToMySQL(cls.db).query_db(query)
        all_places = []
        for row in results:
            #print(row['date_made'])
            all_places.append( cls(row) )
        return all_places
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM places WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM places WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def update(cls, data):
        query = "UPDATE places SET location=%(location)s, date=%(date)s, description=%(description)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM places WHERE users_id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        all_places = []
        for row in results:
            #print(row['date_made'])
            all_places.append( cls(row) )
        return all_places