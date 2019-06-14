#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask import session as login_session
from flask import make_response
from flask import flash
import random
import string
import httplib2
import json
import requests

# Imports for SQLALCHEMY
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item

# Imports for authentication - OAuth2.0
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

app = Flask(__name__)

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

APPLICATION_NAME = "Item-Catalog-App"

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

loggedIn = 0

#Checking if user already exists
def userExists():
    return session.query(User).filter_by(email= \
                                         login_session['email']).one_or_none()


#To update new user record
def createUser(data):
    name = data['name']
    email = data['email']
    img_url = data['picture']
    newUser = User(name=name, email=email, image=img_url)
    session.add(newUser)
    session.commit()


#Creates anti-forgery state token and render login page 
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


#To authenticate user using thirdparty google authentication 
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return responsex
    
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['provider'] = 'google'
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Check is user id in the database or not
    # If not, create user record and add to database
    if not userExists():
       createUser(data)
    
    output = '<center>'
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px; border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    output += '</center>'
    flash("you are now logged in as %s" % login_session['username'])

    # To change 'login' to 'logout' button
    global loggedIn
    loggedIn = 1
    return output


#To disconnect from google authetication service
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Logged out!")
        global loggedIn
        loggedIn = 0
        return redirect(url_for('showCatalog'))
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        redirect(url_for('showLogin'));
        return response


'''APP ROUTES'''

# Home route 
@app.route('/')
@app.route('/catalog/')
@app.route('/category/')
def showCatalog():

    # Checking if user is logged in or not
    global loggedIn
    if 'username' in login_session:
        loggedIn = 1
    
    rowCount = session.query(Item).count()
    latestCount = rowCount
    # Showing latest 6 that has been added to the database
    items = session.query(Item).order_by(desc(Item.id)).limit(6)

    categories = session.query(Category).all()

    return render_template('catalog.html', categories = categories, items= items, loggedIn = loggedIn)

 #Show all items by a particular category
@app.route('/category/<int:category_id>/')
def categoryMenu(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id = category_id)
    global loggedIn
    if 'username' in login_session:
        loggedIn = 1
    
    return render_template('showCategory.html', items = items, category = category, loggedIn = loggedIn)

#Show data of a particular item
@app.route('/category/item/<int:item_id>/')
def showItem(item_id):
    item = session.query(Item).filter_by(id = item_id).one()

    global loggedIn
    if 'username' in login_session:
        loggedIn = 1

    return render_template('showItem.html', item = item, loggedIn = loggedIn)


#To create a new Item
@app.route('/category/item/new/', methods=['GET', 'POST'])
def newItem():
	# Checking if user is logged in, if not asking to login 
    if 'username' not in login_session:
        return redirect('/login')

    # To change 'login' to 'logout' button
    global loggedIn
    if 'username' in login_session:
        loggedIn = 1

    # POST request - Post the items data to database
    if request.method == 'POST':
        cat = session.query(Category).filter_by(name=request.form['cate']).one()
        nItem = Item(
            name = request.form['name'],
            description = request.form['desc'],
            price = request.form['price'],
            category = cat,
            user_id = userExists().id
            )
        
        session.add(nItem)
        session.commit()
        return redirect(url_for('categoryMenu', category_id = cat.id, loggedIn = loggedIn))
    else:
        categories = session.query(Category).all()
        return render_template('newItem.html', categories = categories, loggedIn = loggedIn)


#To edit data of an item
@app.route('/category/item/edit/<int:item_id>', methods=['GET', 'POST'])
def editItem(item_id):

    # Checking if user is logged in, if not asking to login    
    if 'username' not in login_session:
        return redirect('/login')
    
    global loggedIn
    if 'username' in login_session:
        loggedIn = 1

    item = session.query(Item).filter_by(id = item_id).one()
    user = session.query(User).filter_by(id = item.user_id).one()

    # Checking if the email of the creater is same as the email of the logged in user
    if not login_session['email'] == user.email:
        print "You are not creater of this item. Only creater can change edit/delete the item."
        return render_template('showItem.html', item = item, loggedIn = loggedIn, errorMsg='You are not creater of this item. Only creater can update/delete item.')

        
    if request.method == 'POST':
        itemToEdit = session.query(Item).filter_by(id = item_id).one() 
        cat = session.query(Category).filter_by(name=request.form['cate']).one()
        itemToEdit.name = request.form['name'];
        itemToEdit.description = request.form['desc'];
        itemToEdit.price = request.form['price'];
        itemToEdit.category = cat;
        session.commit()
        return redirect('/catalog')
    else:
        item = session.query(Item).filter_by(id = item_id).one()
        categories = session.query(Category).all()
        return render_template('editItem.html', categories = categories, loggedIn = loggedIn, item = item)


#To Confirm if the user that clicked delete is owner of the item or not 
@app.route('/catagory/item/deleteconfirm/<int:item_id>')
def confirmDeleteItem(item_id):
    if 'username' not in login_session:
        return redirect('/login')

    global loggedIn
    if 'username' in login_session:
        loggedIn = 1

    item = session.query(Item).filter_by(id = item_id).one()
    user = session.query(User).filter_by(id = item.user_id).one()

    # Checking if the email of the creater is same as the email of the logged in user
    if not login_session['email'] == user.email:
        return render_template('showItem.html', item = item, loggedIn = loggedIn, errorMsg='You are not creater of this item. Only creater can update/delete item.')
        
    return render_template('deleteItem.html', item = item, loggedIn = loggedIn)


#To delete an item from database
@app.route('/catagory/item/delete/<int:item_id>')
def deleteItem(item_id):
    if 'username' not in login_session:
        return redirect('/login')

    # To change 'login' to 'logout' button
    global loggedIn
    if 'username' in login_session:
        loggedIn = 1

    item = session.query(Item).filter_by(id = item_id).one()
    cat = session.query(Category).filter_by(id = item.category_id).one()
    session.delete(item)
    session.commit()

    return redirect(url_for('categoryMenu', category_id = cat.id, loggedIn = loggedIn))


'''JSON ENDPOINTS'''

#Shows all the items in database
@app.route('/items.json/')
def itemsJSON():
    items = session.query(Item).all()
    return jsonify(Items=[item.serialize for item in items])

#Shows all the items for a particular category 
@app.route('/items/category/<string:category>.json/')
def itemCategoryJSON(category):
    items = session.query(Item).filter_by(category_id=category).all()
    return jsonify(Items=[item.serialize for item in items])

#Shows data of an item for a given category and item id
@app.route('/items/category/<string:category>/<int:itemId>.json/')
def itemJSON(category, itemId):
    item = session.query(Item).filter_by(category_id=category,
                                           id=itemId).first()
    return jsonify(Item=item.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

