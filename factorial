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
