from flask import Flask, render_template
import dbDriver
import routes
app = Flask(__name__, static_url_path="/static/")

@app.route('/')
def __home(*args, **keyargs):
    return routes.home(*args, **keyargs)

@app.route('/login/')
def __login(*args, **keyargs):
    return routes.login(*args, **keyargs)


if __name__ == "__main__":
    app.run(debug=True)