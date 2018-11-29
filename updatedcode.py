from flask import Flask, render_template, request, jsonify
from redis import Redis, RedisError
import hashlib
import requests


app = Flask(__name__)
redis = Redis(host='redis', port=6379)

@app.route('/')
def hello_world():
  return 'Hello from Flask!'

@app.route('/redis/')
def hello():
    count = redis.incr('hits')
    return 'Hello World! I have been seen {} times.\n'.format(count)

@app.route('/factorial/<int:inp>')
def fact(inp):
    try:
        if inp < 0:
            raise ValueError()
    except ValueError:
        return json.dumps({"input":inp, "output": "Must be a non-negative integer"}) 
    else:
        out = math.factorial(inp);
        return json.dumps({"input":inp, "output":out})

@app.route('/fibonacci/<string:inp>/')
def fibonacci(inp):
    try:
        final = int(inp)
        if final <= 0:
            raise ValueError()
    except ValueError:
        return json.dumps({"input":inp, "output":"Value must be an integer, greater than 0"}) 
    else:
        out = [1, 1]
        i = 0
        while (out[-1]+out[-2]) <= final:
            i = out[-1] + out[-2] 
            out.append(i)
        return json.dumps({"input":inp, "output":out})


@app.route('/slack-alert/<string:inp>/')
def slackAlert(inp):
    try:
        url = config.hook
        r = requests.post(url, data=json.dumps({'text':inp}),headers={'Content-Type': 'application/json'})
        return json.dumps({"input":inp, "output":True})
    except Exception as err:
        print(err)
        return json.dumps({"input":inp, "output":False})

@app.route('/md5/<path:inp>')
def hash(inp):
    m = md5.new()
    m.update(inp.encode('utf-8'))
    out = m.hexdigest()
    return json.dumps({"input":inp, "output":out})


@app.route('/is-prime/<int:inp>')
def isPrime(inp):
        try:
                if inp <= 0:
                        raise ValueError()
        except ValueError:
                return json.dumps({"input":inp, "output":"Must be an integer, greater than 0"}) 
        else:
        num = inp
        check = 1
        for i in range(2, num-1):
            if num % i == 0:
                        check = 0
        if inp == 1:
            check = 0
        if check:
            return json.dumps({"input":inp, "output":True})
        else:
            return json.dumps({"input":inp, "output":False})


@app.route('/kv-record/<string:key>', methods=['POST'])
def kv_create(key):
    input = key
    output = False
    err_msg = None
    try:
        # does the key exists already?
        value = redis.get(key)
        if not value == None: 
            err_msg = "Cannot create new record: key already exists."
        else:
            # it's a new key, now create it 
            payload = request.get_json()
            create_red = redis.set(key, payload['value'])
            if create_red == False:
                err_msg = "ERROR: There was a problem creating the value in Redis."
            else:
                output = True
                input = payload
    except RedisError:
        err_msg = "Cannot connect to redis."

    return jsonify(
        input=input,
        output=output,
        error=err_msg
    )

@app.route('/kv-record/<string:key>', methods=['PUT'])
def kv_update(key):
    input = key
    output = False
    err_msg = None
    try:
        # check if key exists
        value = redis.get(key)
        if value == None: 
            err_msg = "Cannot update: key does not exist."
        else:
            # now key exists so update 
            payload = request.get_json()
            update_red = redis.set(key, payload['value'])
            if update_red == False:
                err_msg = "ERROR: Problem updating the value in Redis."
            else:
                output = True
                input = payload
    except RedisError:
        err_msg = "Cannot connect to redis."

    return jsonify(
        input=input,
        output=output,
        error=err_msg
    )

@app.route('/kv-retrieve/<string:key>')
def kv_retrieve(key):
    output = False
    err_msg = None
    try:
        value = redis.get(key)
        if value == None:
            err_msg = "Key does not exist."
        else:
            output = value
    except RedisError:
        err_msg = "Can't connect to redis."

    return jsonify(
        input=key,
        output=output,
        error=err_msg
    )

if __name__ == '__main__':
  app.run(debug=True,host='0.0.0.0')
