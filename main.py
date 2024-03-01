# import json
from flask import Flask, request, jsonify
from utils import custom_csv, custom_credentials, fake_data


app = Flask(__name__)


@app.route('/')
def index():
    with open('templates/index.html') as html_file:
        return html_file.read()
    

@app.route('/generate_csv', methods=['POST'])
def csv_generator():
    data = request.form['csv_data']
    action = request.form['actions']
    custom_csv.generate(data, action)
    return 'CSV file generated, return to the <a href="/">main</a> page'


@app.route('/generate_credentials', methods=['POST'])
def gen_pass():
    qty = int(request.form['qty'])
    return custom_credentials.multiple(qty)


@app.route('/generate_fake_data', methods=['POST'])
def gen_fake():
    data_type = request.form['data_type']
    generated_fake_data = fake_data.generate(data_type=data_type)
    return jsonify(generated_fake_data)
