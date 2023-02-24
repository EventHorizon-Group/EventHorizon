from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.show import Item

@app.route ('/create')
def create():
    return render_template('create.html')

@app.route ('/user/create', methods = ['POST'])
def user_create():
    if not Item.validate_register(request.form):
        return redirect ('/create')

    data={
        'item_name': request.form ['item_name'],
        'description': request.form ['description'],
        'store_name': request.form['store_name'],
        'user_id':session ['user_id']
    }
    Item.create(data)
    return redirect ('/dashboard')

@app.route('/destroy/<int:id>')
def destroy(id):
    data ={
        'id': id
    }
    Item.destroy(data)
    return redirect('/dashboard')

@app.route('/details/<int:id>')
def details(id):
    data ={
        'id': id
    }
    return render_template ('details.html', item=Item.get_description(data))

@app.route('/edit/<int:id>')
def update(id):
    data={
        'id': id
    }
    return render_template ('edit.html', item=Item.get_one(data))

@app.route('/update/<int:id>', methods=['POST'])
def edit(id):
    if not Item.validate_register(request.form):
        return redirect (f'/edit/{id}')
    data={
        'id': id,
        'item_name': request.form ['item_name'],
        'description': request.form ['description'],
        'store_name': request.form['store_name']
    }
    Item.update(data)
    return redirect ('/dashboard')