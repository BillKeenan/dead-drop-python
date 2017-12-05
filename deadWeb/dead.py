from flask import Flask, render_template, send_from_directory
from jinja2 import Template
from flask import jsonify
import os
app = Flask(__name__)

@app.route("/")
def index():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    return render_template('index.htm',title='John Doe')

@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('images', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


@app.route("/drop",methods = ['POST'])
def drop():
    return jsonify(id=1234)

@app.route("/pickup/<id>")
def pickupDrop(id):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    return render_template('index.htm',id=id)



if __name__ == "__main__":
    app.run(host='0.0.0.0')
