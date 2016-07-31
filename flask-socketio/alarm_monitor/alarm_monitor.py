#!/usr/bin/env python

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on available packages.
async_mode = None

if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)

# monkey patching is necessary because this application uses a background
# thread
if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()

import time
from threading import Thread
from flask import Flask, render_template, session, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!' #Seems to be needed for using session: http://flask.pocoo.org/docs/0.10/api/#sessions
socketio = SocketIO(app, async_mode=async_mode)
thread = None

#Alarm Monitor:
#   - Basic concept: serve webpage that shows realtime status of remote alarm nodes
#       - Arduino:
#           - Send alarm messages upon activation
#           - Respond to pings or keepalive messages
#           - send a 'good morning' message when booting 
#       - Flask (flask-socketio):
#           - Listen for incoming alarm messages from Arduino
#           - Send message to client when alarm received
#           - Send keepalive messages and send result to client (maybe do processing here and send desired output only)
#      
#      - Client (javascript / socketio):
#           - display status of alarm(s)
#           - display time since last keepalive (maybe green circle, then yellow and red depending on time since last)
#           - implement a 'ping' button to check on status of Arduino
#           - have a heartbeat symbol that responds to heartbeats from Arduino - size or color of logo would represent freshness 
#               - how about a heart bracketed on left and right by audio symbols - number of arcs repressent freshness - 0 arcs represent overdue heartbeat

#Progress:
#1. Display incoming messages from Arduino (no socketio needed)
#2. constantly update page with latest values as they come in (socketio needed here)
#   - keep straight flask route for incoming data ( @app.route("/alarm") )
#       - in /alarm route use socketio.emit to send broadcast to all clients listening on alarms
#
#Next steps:
#1. improve reliability of Arduino server connection
#   - after restarting server Arduino messages sometimes don't go through
#       - need to flesh this out more. starting Arduino first then server works OK
#       - also am able to restart server and reconnect sometimes
#   ideas:
#       - On Arduino side capture 'message received' portion (last line) of server response
#       - consider issuing reset when connection fails (this isn't always necessary, though <-- gotta figure out when it is.)
#       - add status handler on Arduino
#           - send json list of sensors
#           - may need to use json.dumps for formatting response for javascript use (http://stackoverflow.com/questions/7907596/json-dumps-vs-flask-jsonify)
#2. Develop server:
#   - build a list of connected sensor nodes (dicts): device_id, sensor, pingback address (get from GET request?), status
#       - each sensor node element contains a list of dicts of sensors
#           - incoming messaged parsed for GET values and remote_addr
#           - pack last_rx_data with new info
#           - update nodes
#               - find and update matching node
#               - new node element if not already there
#   - Use list of nodes to populate table (as in logger.py)
#       - for each node have node name as header followed by table of sensors
#       - maybe have each element of table have a custom id or just match sensor name in text (for finding by means of jquery selector)
#       - update table elements as appropriate based on new data
#       - refresh page when list of sensors or nodes changes ( location.reload(true) )
#


nodes = [] # node format {'device_ID':None, 'remote_addr':None, 'sensors':[]} 
            #sensor format: {'sensor_ID':None, 'sensor_type':None, 'sensor_value':None, 'units':None}
last_node = {}
last_rx_data = {'device_ID':None, 'sensor_ID':None, 'sensor_type':None, 'sensor_value':None, 'units':None,'remote_addr':None}

def updateNodes(data): # maybe this should just be part of alarm_message()
    # assumes this format: {'device_ID':None, 'sensor_ID':None, 'sensor_type':None, 'sensor_value':None, 'units':None,'remote_addr':None}
    
    #create a new sensor - if it already exists this will be used to overwrite (update) it
    new_sensor = {'sensor_ID':data['sensor_ID'], 'sensor_type':data['sensor_type'],'sensor_value':data['sensor_value'], 'units':data['units']}
    
    match = {}
    reload_page = False
    node_count = 0 # for debugging/error catching - there should only be one node per device_ID
    sensor_count = 0
    
    # look for matching node, then look for matching sensor
    for node in nodes: 
        if data['device_ID'] == node['device_ID']: #            --- found a matching node ---
            print "Matching node found for device_ID - ", data['device_ID']
            node_count += 1
            sensors = node['sensors'] # get list of sensors for this node (replace the existing list with this list before finishing)
            
            for index, sensor in enumerate(sensors):
                if sensor['sensor_ID'] == data['sensor_ID']:#   --- found a matching sensor ---
                    sensor_count += 1
                    sensors[index] = new_sensor # replace the old sensor entry with the new one
                    print "matching sensor found for sensor_ID - ", data['sensor_ID']
            if sensor_count == 0:#                             --- matching node but no matching sensor --- 
                sensors.append(new_sensor)
                print "no matching sensor found. appending new sensor: ", new_sensor
                #reload_page = True #reload page to show new sensor

            node['sensors'] = sensors # replace existing list with new (updated) list
            print "updated node: ", node
            
    if node_count > 1:
        raise Exception('Too many node matches found for device')

    if node_count == 0: #                                   --- no matching node ---
        # create new node with new sensor:
        new_node = {'device_ID':data['device_ID'],'remote_addr':data['remote_addr'], 'sensors':[new_sensor]}
        nodes.append(new_node)        
        print "no matches found. added new node: ", new_node
        # reload_page = True
        
    # find node with matching device_ID
    # if no match 
    #   - create new node
    #   - reload_page = True
    # if match look for matching sensor
    #   - update matching sensor / check for matching remote addr
    #   - if no matching sensor 
    #       - create 
    #       - reload_page = True
    # update
    
    return reload_page
    

@app.route("/test")
def test():
    # see :
    # http://flask.pocoo.org/docs/0.10/reqcontext/
    # http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
    # http://werkzeug.pocoo.org/docs/0.11/datastructures/#werkzeug.datastructures.MultiDict
    if 'reload' in request.args.values()[0]: #for testing 
        print('issuing reload signal')
        socketio.emit('reload_page')
    print "query_string: ", request.query_string
    print "args: ", request.args.items()
    print "keys: ", request.args.keys()
    print "values: ", request.args.listvalues() # there is also a values() method
    print "args as a dict: ", request.args.to_dict()
    print "remote address: ", request.remote_addr 
    #print "request.event", request.event.keys()
    return jsonify({'ip': request.remote_addr, "args: ": request.args.items()}), 200

@app.route('/')
def index():
    return render_template('index.html')

# To do: should change alarm to alarms. On GET provide, say, a list of current nodes. On POST do some sort of update of alarm
@app.route('/alarm')
def alarm_message():    
    print
    print "----------- alarm message received -----------"
    print "--- query_string: ", request.query_string
    print "--- remote address: ", request.remote_addr
    print "----------------------------------------------"
    
    request_dict = request.args.to_dict()
    
    #pack query string into last_rx_data: 
    last_rx_data = {'device_ID':None, 'sensor_ID':None, 'sensor_type':None, 'sensor_value':None, 'units':None,'remote_addr':None} # reset dict
    last_rx_data['remote_addr'] = request.remote_addr # could use dict.update() but I think I want to catch it when message keys don't match
    for k,v in request_dict.items():
        last_rx_data[k] = v
    
    reload_page = False
    
    # if node update indicates new node or new sensor, toggle flag to indicate reload needed
    reload_page = updateNodes(last_rx_data)
    
    if reload_page == True:
        # reload page to catch and display new sensors or nodes
        socketio.emit('reload_page',{}) # shouldn't need payload but add ,{} if necessary
        
    socketio.emit('alarm_received', 'motion sensed') #hope it's ok to send this right after reload
        
    return 'message received'

@socketio.on('connection event')
def handleConnectionEvent(message):
    print "connection event: ", message

@app.route("/debug") 
def debug():
    raise Exception('Nothing to see here. Move along') #used for debugging in browser - click on little console logo at the right
    '''Then you can do cool stuff like:
        >>> cur = g.db.execute('select device_ID, sensor_ID, sensor_type, sensor_value, units, timestamp from entries order by id desc')
        >>> entry = cur.fetchone()
        also: dump(g), dump(session), dir(), globals(), locals(), dir(g), dir(session), 
    '''
    return

@socketio.on('message')
def handle_message(message):
    print 'received message: ', message['data']


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0',debug=True)


#Snippets:
"""
    
def background_thread():
    # Example of how to send server generated events to clients.
    # Should probably just drop this for now.
    # might be interesting to implement some sort of heartbeat function on Arduino but that wouldn't require
    # flask based thread.
    # might be cool to add a ping button to webpage that would change state based on response from Arduino
    count = 0
    while True:
        time.sleep(10)
        count += 1
        socketio.emit('my response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test') # namespace should

def index():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.daemon = True
        thread.start()
    return render_template('index.html')

"""
