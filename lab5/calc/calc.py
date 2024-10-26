from flask import Flask, request, make_response, jsonify
import random, time, os, threading, requests

app = Flask(__name__)

@app.route('/calc')
def calc_home():
    return "This is the Calc service!"
@app.route('/add')
def add():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a and b:
        # Call save_last and capture the success status and error message
        success, error_message = save_last("upper", f"({a})", res)
        
        if success:
            return make_response(jsonify(s=res,redis_message=success or error_message), 200)
        else:
            # Return the error message in the response if saving failed
            return make_response(jsonify(error=error_message), 500)
    else:
        return make_response('Invalid input\n', 400) #HTTP 400 BAD REQUEST

@app.route('/sub')
def sub():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a and b:
        # Call save_last and capture the success status and error message
        success, error_message = save_last("upper", f"({a})", res)
        
        if success:
            return make_response(jsonify(s=res,redis_message=success or error_message), 200)
        else:
            # Return the error message in the response if saving failed
            return make_response(jsonify(error=error_message), 500)

@app.route('/mul')
def mul():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a and b:
        # Call save_last and capture the success status and error message
        success, error_message = save_last("upper", f"({a})", res)
        
        if success:
            return make_response(jsonify(s=res,redis_message=success or error_message), 200)
        else:
            # Return the error message in the response if saving failed
            return make_response(jsonify(error=error_message), 500)
    else:
        return make_response('Invalid input\n', 400)

@app.route('/div')
def div():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a and b:
        if b == 0:
            return make_response('Division by zero\n', 400)
        # Call save_last and capture the success status and error message
        success, error_message = save_last("upper", f"({a})", res)
        
        if success:
            return make_response(jsonify(s=res,redis_message=success or error_message), 200)
        else:
            # Return the error message in the response if saving failed
            return make_response(jsonify(error=error_message), 500)
    else:
        return make_response('Invalid input\n', 400)

@app.route('/mod')
def mod():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a and b:
        if b == 0:
            return make_response('Division by zero\n', 400)
        # Call save_last and capture the success status and error message
        success, error_message = save_last("upper", f"({a})", res)
        
        if success:
            return make_response(jsonify(s=res,redis_message=success or error_message), 200)
        else:
            # Return the error message in the response if saving failed
            return make_response(jsonify(error=error_message), 500)
    else:
        return make_response('Invalid input\n', 400)

@app.route('/random')
def rand():
    a = request.args.get('a', type=int)
    b = request.args.get('b', type=int)
    if a and b:
        if a > b:
            return make_response('Invalid input\n', 400)
        res = random.randint(a, b)
        # Call save_last and capture the success status and error message
        success, error_message = save_last("upper", f"({a})", res)
        
        if success:
            return make_response(jsonify(s=res,redis_message=success or error_message), 200)
        else:
            # Return the error message in the response if saving failed
            return make_response(jsonify(error=error_message), 500)
    else:
        return make_response('Invalid input\n', 400)

@app.route('/last')
def last():
    try:
        with open('last.txt', 'r') as f:
            return make_response(jsonify(s=f.read()), 200)
    except FileNotFoundError:
        return make_response('No operations yet\n', 404)


def save_last(op, args, res):
    # Construct the data to send to the last service
    data = {
        "s": f"{op}{args}={res}"
    }
    
    try:
        response = requests.post("http://last_service:5000/store", json=data)
        response.raise_for_status()
        return response.json().get('message'), None
    except requests.exceptions.RequestException as e:
        error_message = f"Failed to save data to last service: {e.response.text if e.response else str(e)}"
        print(error_message) 
        return False, error_message  

if __name__ == "__main__":
    pass
