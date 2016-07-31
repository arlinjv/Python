from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello():
    print "query_string: ", request.query_string
    print "args: ", request.args.items()
    print "keys: ", request.args.keys()
    print "values: ", request.args.listvalues()
    print "args as a dict: ", request.args.to_dict()
    
    return request.query_string
    
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug = True)
