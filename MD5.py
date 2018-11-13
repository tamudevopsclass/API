
@app.route('/md5/<path:inp>')
def hash(inp):
    m = md5.new()
    m.update(inp.encode('utf-8'))
    out = m.hexdigest()
    return json.dumps({"input":inp, "output":out})
