import os, redis
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Connect to Redis
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = os.getenv("REDIS_PORT", 6379)
redis_client = redis.Redis(host=redis_host, port=int(redis_port))

@app.route('/redis-test')
def redis_test():
    # Example: Set and get a value from Redis
    redis_client.set('test_key', 'Hello from Redis!')
    return redis_client.get('test_key') or "Could not fetch data from Redis"

@app.route('/store', methods=['POST'])
def store_operation():
    # Get the JSON data from the request
    data = request.get_json()
    
    if not data or 's' not in data:
        return jsonify({"error": "Invalid input format"}), 400
    
    # Parse the operation string
    try:
        # Example input: "upper(a)=A"
        operation_part, res = data['s'].split('=')
        op, args_str = operation_part.split('(')
        args = args_str.strip(')').split(',')
        
        # Prepare data for Redis
        timestamp = datetime.now().isoformat()
        op_dict = {
            "op": op,
            "args": args,
            "res": res
        }
        
        # Save to Redis
        redis_client.set(timestamp, str(op_dict))
        
        return jsonify({"message": "Data stored successfully", "timestamp": timestamp, "data": op_dict}), 201
    
    except ValueError as e:
        return jsonify({"error": "Error parsing input string"}), 400

@app.route('/records', methods=['GET'])
def get_all_records():
    # Fetch all records from Redis
    all_keys = redis_client.keys()
    all_records = {}
    
    for key in all_keys:
        record = redis_client.get(key).decode('utf-8')
        all_records[key.decode('utf-8')] = record
    
    return jsonify(all_records), 200
if __name__ == "__main__":
    pass
