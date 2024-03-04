from flask import Flask, request, jsonify
from utils import custom_csv, custom_credentials, fake_data, custom_json


app = Flask(__name__)


@app.route('/')
def index():
    with open('templates/index.html') as html_file:
        return html_file.read()
    

@app.route('/generate_csv', methods=['POST'])
def generate_csv():
    data = request.form['csv_data']
    action = request.form['actions']
    custom_csv.generate(data=data, action=action)
    return 'CSV file generated, return to the <a href="/">main</a> page'


@app.route('/generate_credentials', methods=['POST'])
def generate_credentials():
    qty = int(request.form['qty'])
    return custom_credentials.multiple(number=qty)


@app.route('/generate_fake_data', methods=['POST'])
def generate_fake_data():
    data_type = request.form['data_type']
    return fake_data.generate(data_type=data_type)


@app.route('/parse_json', methods=['POST'])
def parse_json():
    # Получаем строку с полями из HTML формы
    fields_input = request.form['cnvrt']
    # Удаляем пробелы в начале и в конце каждого значения и разделяем строку на список
    fields_list = [field.strip() for field in fields_input.split(',')]

    uploaded_file = request.files['file']
    filename = uploaded_file.filename
    uploaded_file.save(filename)
    return custom_json.read(FILENAME=filename, FIELDS_LIST=fields_list)


if __name__ == "__main__":
    app.run(debug=True, port=5000)