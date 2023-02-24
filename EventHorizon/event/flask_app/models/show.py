from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Item:
    def __init__(self,data):
        self.id = data['id']
        self.item_name = data['item_name']
        self.description = data['description']
        self.store_name = data['store_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.userself = None

    @classmethod
    def create(cls, data):
        query = "INSERT INTO items (item_name, description, store_name, user_id) VALUES (%(item_name)s, %(description)s, %(store_name)s, %(user_id)s);"
        results = connectToMySQL('family_registration').query_db(query,data)
        print (results)
        return results

    @classmethod
    def get_users_and_items(cls):
        query = "SELECT * FROM items JOIN users on users.id = items.user_id;"
        results = connectToMySQL('family_registration').query_db(query)
        print (results)
        all_items = []

        for pho in results:
            one_item = cls(pho)
            user_data ={
                'id':pho['users.id'], 
                'first_name':pho['first_name'],
                'last_name':pho['last_name'],
                'email':pho['email'],
                'password':None,
                'created_at': pho['users.created_at'],
                'updated_at':pho['users.updated_at']
            }
            user_obj = user.User(user_data)
            one_item.userself = user_obj
            all_items.append(one_item)
        return all_items

    @classmethod
    def destroy (cls, data):
        query = "DELETE FROM items WHERE id = %(id)s;"
        return connectToMySQL('family_registration').query_db(query, data)

    @classmethod
    def get_description (cls, data):
        query = "SELECT * FROM items JOIN users on users.id = items.user_id WHERE items.id = %(id)s;"
        result = connectToMySQL('family_registration').query_db(query, data)

        row = cls (result[0])

        one_user_data={
            'id':result[0]['users.id'],
            'first_name':result[0]['first_name'],
            'last_name':result[0]['last_name'],
            'email':result[0]['email'],
            'password': None,
            'created_at':result[0]['users.created_at'],
            'updated_at':result[0]['users.updated_at']
        }
        user_obj=user.User(one_user_data)
        row.userself = user_obj
        return row

    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM items WHERE id = %(id)s;"
        result = connectToMySQL('family_registration').query_db(query,data)
        return cls(result[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE items SET item_name=%(item_name)s,description=%(description)s,store_name=%(store_name)s WHERE id = %(id)s;"
        return connectToMySQL('family_registration').query_db(query,data)


    @staticmethod
    def validate_register(tv):
        is_valid = True # we assume this is true
        if len(tv['item_name']) < 3:
            flash("Item must be at least 2 characters")
            is_valid= False
        if len(tv['description']) < 3:
            flash("Description must be at least 10 characters")
            is_valid= False
        if len(tv['store_name']) < 3:
            flash("Store Name must be at least 2 characters")
            is_valid= False
        return is_valid