from flask import Flask, request, jsonify
from redis import Redis, RedisError
import os
import socket
import md5
import math

redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)
import requests
import json

@app.route("/")
def hello():
	try:
		visits = redis.incr("counter")
	except RedisError:
		visits = "<i>cannot connect to Redis, counter disabled</i>"

	html =  "<h3> Hello {name}!</h3>" \
		"<b>Hostname:</b> {hostname}<br/>" \
		"<b>Visits:</b> {visits}"
	return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)

@app.route('/md5/<path:inp>')
def hash(inp):
	m = md5.new()
	m.update(inp.encode('utf-8'))
	out = m.hexdigest()
	return json.dumps({"input":inp, "output":out})

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

@app.route('/fibonacci/<string:inp>')
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


@app.route('/slack-alert/<string:inp>')
def slackAlert(inp):
	url= 'https://hooks.slack.com/services/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'
	slack_message = {'text' :inp}
	if requests.post(url,data=json.dumps(slack_message)):
		print(inp)
		return json.dumps({"input": inp, "output":True})
	else:
		return json.dumps({"input":inp, "output":False})

@app.route('/is-prime/<string:inp>')
def isPrime(inp):
	try:
		num = int(inp)
		if num <= 0:
			raise ValueError()
	except ValueError:
		return json.dumps({"input":inp, "output":"Value must be an integer, greater than 0"})
	if inp == 1:
		return json.dumps({"input":inp, "output":False})
	else:
		check = 1
		for i in range(2, num-1):
			if num % i == 0:
				check = 0
		if check:
			return json.dumps({"input":inp, "output":True})
		else:
			return json.dumps({"input":inp, "output":False})

@app.route('/kv-record/<string:key>', methods = ["POST", "PUT"])
def record(key):
	try:
		data = request.get_json(force=True)
		value = data['value']
		key = data['key']
		if request.method == "POST":
			if redis.exists(key):
				return json.dumps({"input": "new-key", "output": False, "error": "Unable to add pair: key already exists."})
			else:
				redis.set(key, value)
				return json.dumps({"input": "new-key", "output": True})

		elif request.method == "PUT":
			if redis.exists(key):
				redis.set(key, value)
				return json.dumps({"input": "existing-key", "output": True})
			else:
				return json.dumps({"input": "existing-key", "output": False, "error": "Unable to update value: key does not exist."})
		else:
			raise
			
	except Exception as error:
		return json.dumps({"output": False, "error": str(error)})
		

@app.route('/kv-retrieve/<string:key>')
def retrieve(key):
	try:
		if redis.exists(key):
			return json.dumps({"input": "retrieve-value", "output": redis.get(key)})
		else:
			return json.dumps({"input": "retrieve-value", "output": False, "error": "Unable to update value: key does not exist."})
			
	except Exception as error:
		return json.dumps({"output": False, "error": str(error)})



if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)	

