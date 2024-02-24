# import json
from flask import Flask, request, jsonify

import fake_data
import generate_csv
import generate_passwords


app = Flask(__name__)


@app.route('/')
def index():
    with open('index.html') as html_file:
        return html_file.read()
    

@app.route('/generate_csv', methods=['POST'])
def csv_generator():
    print(request.form)
    data = request.form['csv_data']
    action = request.form['actions']
    generate_csv.generate(data, action)
    return 'CSV file generated, return to the <a href="/">main</a> page'


@app.route('/passw', methods=['POST'])
def gen_pass():
    qty = int(request.form['qty'])
    print(qty)
    return generate_passwords.multiple(qty)

@app.route('/fake_data', methods=['POST'])
def gen_fake():
    data_type = request.form['data_type']
    generated_fake_data = fake_data.generate(data_type=data_type)
    return jsonify(generated_fake_data)