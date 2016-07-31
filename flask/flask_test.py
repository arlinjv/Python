from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
@app.route("/alarm")
def hello():
    # see :
    # http://flask.pocoo.org/docs/0.10/quickstart/#accessing-request-data
    # http://flask.pocoo.org/docs/0.10/reqcontext/
    # http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
    # http://werkzeug.pocoo.org/docs/0.11/datastructures/#werkzeug.datastructures.MultiDict
    print "query_string: ", request.query_string
    print "args: ", request.args.items()
    print "keys: ", request.args.keys()
    print "values: ", request.args.listvalues() # there is also a values() method
    print "args as a dict: ", request.args.to_dict()
    print "full path", request.full_path
    print "host: ", request.host
    print "remote address: ", request.remote_addr
    # print "values: ", request.values
    return jsonify({'ip': request.remote_addr, "args: ": request.args.items()}), 200
    #return request.query_string
    
@app.route("/push")
def receive_data(): 
    return 'Hello'
    
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug = True)
