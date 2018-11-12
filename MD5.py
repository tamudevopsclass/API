
@app.route('/md5/<input>')
def md5(input):
    if input:
      out = md5.new(input).digest()
      return json.dumps({"input":input, "output":out})
    else 
     return "Error: input a string"

