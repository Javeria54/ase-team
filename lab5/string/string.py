from flask import Flask, request, make_response, jsonify
import random, time, os, threading, requests ,json


app = Flask(__name__)

@app.route('/test')
def calc_home():
    return "This is the String service checked!"

@app.route('/concat')
def concat():
    a = request.args.get('a', type=str)
    b = request.args.get('b', type=str)
    if a and b:
        res = a+b
        success, error_message = save_last("upper", f"({a})", res)
    
        if success:
            return make_response(jsonify(s=res,redis_message=success or error_message), 200)
        else:
            # Return the error message in the response if saving failed
            return make_response(jsonify(error=error_message), 500)
    else:
        return make_response('Invalid input\n', 400)

@app.route('/upper')
def upper():
    a = request.args.get('a', 0, type=str)
    res = a.upper()
    # Call save_last and capture the success status and error message
    success, error_message = save_last("upper", f"({a})", res)
    
    if success:
        return make_response(jsonify(s=res,redis_message=success or error_message), 200)
    else:
        # Return the error message in the response if saving failed
        return make_response(jsonify(error=error_message), 500)

@app.route('/lower')
def lower():
    a = request.args.get('a', 0, type=str)
    res = a.lower()
    success, error_message = save_last("upper", f"({a})", res)
    
    if success:
        return make_response(jsonify(s=res,redis_message=success or error_message), 200)
    else:
        # Return the error message in the response if saving failed
        return make_response(jsonify(error=error_message), 500)


@app.route('/reduce')
def reduce():
    op = request.args.get('op', type=str)
    lst = request.args.get('lst', type=str)
    if op and lst:
        lst = eval(lst)
        if op == 'add':
            res = sum(lst)
            response =  make_response(jsonify(s=res), 200)
        elif op == 'sub':
            res = lst[0] - sum(lst[1:])
            response = make_response(jsonify(s=res), 200)
        elif op == 'mul':
            res = 1
            for i in lst:
                res *= i
            response = make_response(jsonify(s=res), 200)
        elif op == 'div':
            res = lst[0]
            for i in lst[1:]:
                if i == 0:
                    return make_response('Division by zero\n', 400)
                res /= i
            response = make_response(jsonify(s=res), 200)
        elif op == 'concat':
            res = ''
            for i in lst:
                res += i
            response = make_response(jsonify(s=res), 200)
        else:
            return make_response(f'Invalid operator: {op}', 400)
        success, error_message = save_last("upper", f"({a})", res)
    
        if success:
            return make_response(jsonify(s=res,redis_message=success or error_message), 200)
        else:
            # Return the error message in the response if saving failed
            return make_response(jsonify(error=error_message), 500)
    else:
        return make_response('Invalid operator\n', 400)

@app.route('/crash')
def crash():
    def close():
        time.sleep(1)
        os._exit(0)
    thread = threading.Thread(target=close)
    thread.start()
    ret = str(request.host) + " crashed"
    return make_response(jsonify(s=ret), 200)

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
