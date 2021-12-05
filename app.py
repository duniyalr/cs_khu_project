from flask import Flask, render_template
import dbDriver

app = Flask(__name__, static_url_path="/static/")

@app.route('/')
def __home():
    return render_template('home.html   ')

@app.route('/login/')
def __login():
    return 'this is login page'


if __name__ == "__main__":
    app.run()