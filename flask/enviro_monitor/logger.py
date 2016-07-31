# review these imports - probably don't need some - copied a lot from http://flask.pocoo.org/docs/0.10/tutorial/setup/#tutorial-setup
from flask import Flask, request, g, redirect, url_for, abort, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import sqlite3
from contextlib import closing #needed for enabling init_db code. see - http://flask.pocoo.org/docs/0.10/tutorial/dbinit/#tutorial-dbinit

#configuration
DATABASE = 'sensor_data.db'
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
LOGIN_DISABLED = 'True' #trying to disable login due to 401 error when trying to add from esp8266
TESTING = 'True'        # ditto

app = Flask(__name__)
app.config.from_object(__name__) # looks for uppercase variables

app.debug = True

#toolbar = DebugToolbarExtension(app)

def connect_db():
    #return sqlite3.connect(app.config['DATABASE']) # should work now that script contains app.config above
    return sqlite3.connect(DATABASE)

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f: #need to fix schema for my purposes
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
    return db

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)
    
    
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route("/", methods=['GET', 'POST'])
@app.route("/<debug>")
def show_entries(debug = False):
    
    show_entries.last_request = request 
    # To do: use above to implement cascaded filtering on display page (something like if lr has key device_ID then don't show form for device id this time)
    
    if request.method == 'GET':         #should usually be GET
        query = request.args.to_dict()  #so this should usually be at least an empty dict
    
    # gonna get ugly here - should probably find a way to generalize the next two sections    
    if query.has_key('device_ID') and query['device_ID'] != 'all':      # this should break if there is a post request
        cur = g.db.execute('select timestamp, device_ID, sensor_ID, sensor_type, sensor_value, units from entries where device_ID=? order by timestamp desc', (query['device_ID'],))
        print "showing entries for ", query['device_ID']
    elif query.has_key('sensor_ID') and query['sensor_ID'] != 'all':
        cur = g.db.execute('select timestamp, device_ID, sensor_ID, sensor_type, sensor_value, units from entries where sensor_ID=? order by timestamp desc', (query['sensor_ID'],))
        print "showing entries for ", query['sensor_ID']
    elif query.has_key('sensor_type') and query['sensor_type'] != 'all':
        cur = g.db.execute('select timestamp, device_ID, sensor_ID, sensor_type, sensor_value, units from entries where sensor_type=? order by timestamp desc', (query['sensor_type'],))
        print "showing entries for ", query['sensor_type']
    else: #just show everything
        cur = g.db.execute('select timestamp, device_ID, sensor_ID, sensor_type, sensor_value, units from entries order by timestamp desc') #should order by timestamp
    
    entries = cur.fetchall()

    cur = g.db.execute('select * from entries')
    columns = [description[0] for description in cur.description] #http://stackoverflow.com/questions/7831371/is-there-a-way-to-get-a-list-of-column-names-in-sqlite

    cur = g.db.execute('select distinct device_ID from entries')
    IDs = cur.fetchall() #this returns a list of tuples which don't print nicely
    device_IDs = [ID[0] for ID in IDs] # convert each tuple to a string - http://stackoverflow.com/questions/6547658/how-to-remove-u-from-sqlite3-cursor-fetchall-in-python

    cur = g.db.execute('select distinct sensor_ID from entries')
    IDs = cur.fetchall()
    sensor_IDs = [ID[0] for ID in IDs]
    
    cur = g.db.execute('select distinct sensor_type from entries')
    types = cur.fetchall()
    sensor_types = [t[0] for t in types]
    

    if debug:
        raise Exception('Invoking debugger') # now should have access to cur and columns, etc. via dump()
    
    return render_template('show_entries.html', entries=entries, columns=columns, device_IDs=device_IDs, sensor_IDs=sensor_IDs, sensor_types=sensor_types)

@app.route('/add', methods=['GET'])
def add_entry():
    
    '''
    if not session.get('logged_in'): #figure out how to disable this
        abort(401)
    '''
        
    query = request.args.to_dict()
    
    print "Query string as dict: ", query
    
    record = {'device_ID':'NULL','sensor_ID':'NULL', 'sensor_type':'NULL', 'sensor_value':'NULL', 'units':'NULL'}
    for key in query.keys():
        record[key] = query[key]
    
    print "Record to send to db: ", record
    
    g.db.execute('insert into entries (device_ID, sensor_ID, sensor_type, sensor_value, units) values (?,?,?,?,?)', [record['device_ID'],record['sensor_ID'],record['sensor_type'],record['sensor_value'],record['units']])
    g.db.commit()
    '''
    print "Title: ", query['title']
    print "Title: ", query['text']
   
    g.db.execute('insert into entries (title, text) values (?, ?)', [query['title'], query['text']])
    g.db.commit()
    flash('New entry was successfully posted') 
    '''
    
    return "OK" #redirect(url_for('show_entries'))


@app.route("/test") #rename debug?
def test():
    raise Exception('Nothing to see here. Move along') #used for debugging in browser - click on little console logo at the right
    '''Then you can do cool stuff like:
        >>> cur = g.db.execute('select device_ID, sensor_ID, sensor_type, sensor_value, units, timestamp from entries order by id desc')
        >>> entry = cur.fetchone()
        also: dump(g), dump(session), dir(), globals(), locals(), dir(g), dir(session), 
    '''
    return

@app.route("/push")
def receive_data(): 
    return "Hello"
    
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug = True)
