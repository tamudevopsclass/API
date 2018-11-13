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

