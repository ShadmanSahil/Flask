from flask import Flask

app=Flask(__name__)

@app.route('/register', methods=['GET','POST'])
def register():
    pass

@app.route('/login', methods=['GET','POST'])
def login():
    pass

if __name__=='__main__':
    app.run(debug=True)
