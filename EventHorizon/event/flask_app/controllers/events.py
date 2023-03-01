from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.event import Event

@app.route ('/event/new')
def create():
    return render_template('create.html')


@app.route ('/event/create', methods = ['POST'])
def user_create():
    if not Event.validate_register(request.form):
        return redirect ('/event/create')


    create_data={
        'event_name': request.form ['event_name'],
        'description': request.form ['description'],
        'member_num': request.form['member_num'],
        'location': request.form['location'],
        'date': request.form['date'],
        'users_id': session['user_id']
    }
    event_id = Event.create(create_data)

    add_member_data = {
        "events_id": event_id,
        "users_id": session['user_id']
    }

    Event.add_memeber(add_member_data)

    return redirect ('/dashboard')

@app.route('/event/destroy/<int:id>')
def destroy(id):
    data ={
        'id': id
    }
    Event.destroy(data)
    return redirect('/dashboard')

@app.route('/event/details/<int:id>')
def event_details(id):
    data ={
        'id': id
    }
    return render_template ('event_details.html', event=Event.get_one(data))

@app.route('/event/edit/<int:id>')
def update(id):
    data={
        'id': id
    }
    return render_template ('edit.html', event=Event.get_one(data))

@app.route('/event/update/<int:id>', methods=['POST'])
def edit(id):
    if not Event.validate_register(request.form):
        return redirect (f'/event/edit/{id}')
    data={
        'id': id,
        'event_name': request.form ['event_name'],
        'description': request.form ['description'],
        'member_num': request.form['member_num'],
        'location': request.form['location'],
        'date': request.form['date']
    }
    Event.update(data)
    return redirect ('/dashboard')

@app.route('/event/bulletin')
def event_bulletin():
    data = {
        'id': session["user_id"]
    }

    logged_in_user=User.get_user_with_events(data)
    events=Event.get_users_and_events()

    print(logged_in_user.joined_events)
    print(events)

    # for event in events:
    #     if event not in logged_in_user.joined_events:
    #         print("User has NOT joined event")
    #     else:
    #         print("User has joined Event")
        
    

    return render_template('bulletin.html', events=events, logged_in_user=logged_in_user)